import logging
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form

from isaw.policy import MessageFactory as _
from isaw.policy.setuphandlers import setup_saml2


logger = logging.getLogger(__name__)


class SetupSAML2(form.Form):
    """Tool for copying member email addresses to the login field.
    """

    # fields = field.Fields(ISyncEmailToLoginForm)
    label = _(u"Set up SAML2 (runs a setuphandler function)")
    ignoreContext = True  # Don't try to pre-populate form values from context
    msgTemplate = u"Done."

    @button.buttonAndHandler(_(u"Set 'em up"))
    def run(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        setup_saml2(portal)
        successMsg = _(self.msgTemplate)
        logger.info(successMsg)
        self.status = successMsg
        self.request.response.redirect('{0}/@@{1}'.format(
            self.context.absolute_url(), self.__name__))

        return u''

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Setup cancelled."), type="info")
        self.request.response.redirect(self.context.absolute_url())
        return u''
