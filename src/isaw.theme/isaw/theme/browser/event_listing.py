# -*- coding: utf-8 -*-
"""View providing a listing of events

Suitable for folders or collections

Also includes a viewlet which will show the "featured_item" returned by 
the method on the view.
"""
from DateTime import DateTime

from zope.interface import implements

from isaw.theme.browser.interfaces import IEventListingView
from isaw.theme.browser.tiled_view import TiledListingView


class EventListingView(TiledListingView):
    """view class"""
    implements(IEventListingView)
    image_scale = 'blogtile'
    image_placeholder = '<div class="blogtile_placeholder">&nbsp;</div>'
    batch_size = 12 
    page = 1

    def format_date(self, date):
        if date:
           date = self.translation_service.ulocalized_time(
                DateTime(date), True, False, self.context, domain='plonelocales')
        return date

    def listings(self, b_start=None, b_size=None):
        """get a page of listings"""
        if b_size == None:
            b_size = self.batch_size
        if b_start == None:
            b_start = (getattr(self, 'page', 1) - 1) * b_size + 1
        if self.context.portal_type == 'Folder':
            content_filter = {
                'b_start': b_start,
                'b_size': b_size,
                'portal_type': 'Event',
                'sort_on': 'start',
                'sort_order': 'ascending',
                'review_state': 'published',
                'start': {'query': DateTime(), 'range': 'min'},
            }
            items = self.context.getFolderContents(
                content_filter, batch=True
            )
        elif self.context.portal_type == 'Topic':
            if b_start and not self.request.get('b_start'):
                self.request['b_start'] = b_start
            items = self.context.queryCatalog(self.request, True, b_size)
        elif self.context.portal_type == 'Collection':
            items = self.context.results(True, b_start, b_size)
        else:
            items = []
        return items
