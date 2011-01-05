from DateTime import DateTime

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from isaw.theme.browser.interfaces import IUtilsView


class UtilsView(BrowserView):
    """See `IUtilsView` for documentation
    """
    implements(IUtilsView)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.portal_catalog = getToolByName(context, 'portal_catalog')

    def getUpcomingEvents(self, limit=2):
        """Grabbing latests news stuff for the news landing page"""
        asdasfdsfa
        return self.portal_catalog(portal_type=['Conference',
                                                'Exhibition',
                                                'Event',
                                                'General',
                                                'Lecture',
                                                'Performance',
                                                'Seminar',
                                                'Sponsored'],
                                   end={'query': DateTime(), 'range': 'min'},
                                   sort_on='start',
                                   review_state='published')[:limit]


