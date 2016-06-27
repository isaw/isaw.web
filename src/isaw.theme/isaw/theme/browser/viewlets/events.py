from Acquisition import aq_inner
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ..interfaces import IISAWSettings


class SearchEvents(ViewletBase):
    render = ViewPageTemplateFile('events.pt')

    def is_event_listing(self):
        return self.view.__name__ == 'event-listing'
