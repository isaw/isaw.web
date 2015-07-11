from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ..interfaces import IISAWSettings


class EmergencyMessage(ViewletBase):
    render = ViewPageTemplateFile('emergency.pt')

    def message(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IISAWSettings, False)
        message = getattr(settings, 'emergency_message', '')
        closed = self.request.cookies.get("isaw-emergency-read", None)
        if closed:
            message = ''
        return message.strip()
