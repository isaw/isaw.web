from zope.interface import Interface
from zope import schema
from zope.component import getUtility
from Products.Five.browser import BrowserView

import xmlrpclib
import random

from zope.formlib import form
from five.formlib import formbase

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

issue_tracker = xmlrpclib.ServerProxy('http://admin:M4d!s0n@automaton.isaw.nyu.edu:8082/help/', allow_none=True)

usercode = random.randint(10000, 99999)
def checkEmailAddress(value):
    portal = getUtility(ISiteRoot)

    reg_tool = getToolByName(portal, 'portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True

class ISiteWideUserForm(Interface):

    fullname = schema.TextLine(title=u"Fullname",
                            description=u"Enter full name, e.g. John Smith.",
                            required=True)

    email = schema.ASCIILine(title=u"Email",
                            description=u"Enter an email address. This resembles netid@nyu.edu",
                            required=True,
                            constraint=checkEmailAddress)

class SiteWideUserForm(formbase.PageForm):
    form_fields = form.FormFields(ISiteWideUserForm)

    label = (u"Add a new sitewide user (website, copiers, ticket system)")
    description = (u"Onboard a new sitewide user to all ISAW systems")
    

    @form.action(u"Add new user")
    def action_send(self, action, data):
        """ Add's new user and then an email is sent """
        context = aq_inner(self.context)
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()

        user_id = data['fullname']
        email = data['email']

        """ The usercode paradigm hopefully fades away in the future and is sync'd via SSO """

        # Random five digit int for usercode
        print usercode 
        # Issue Tracker Create
        issue_tracker.create('user', "username=%s" % email, 
                                    "address=%s" % email, 
                                    "realname=%s" % user_id, 
                                    "password=%s" % usercode,
                                    "organisation=nyu.edu",
                                    "roles=User" )
            
        IStatusMessage(self.request).addStatusMessage(_(u"Sitewide user " + user_id + " added."), type='info')

        self.request.response.redirect(portal.absolute_url() + '/@@sitewide-user')
        return

class SiteWideUser(BrowserView):
    pass
