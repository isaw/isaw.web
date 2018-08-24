# -*- coding: utf-8 -*-
"""View providing a listing of events

Suitable for folders or collections

Also includes a viewlet which will show the "featured_item" returned by
the method on the view.
"""
from DateTime import DateTime

from zope.component import queryUtility
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from plone.batching import Batch
from plone.registry.interfaces import IRegistry

from isaw.theme.browser.interfaces import IEventListingView
from isaw.theme.browser.interfaces import IISAWSettings
from isaw.theme.browser.tiled_view import TiledListingView


class EventListingView(TiledListingView):
    """view class"""
    implements(IEventListingView)
    image_scale = 'blogtile'
    image_placeholder = '<div class="blogtile_placeholder">&nbsp;</div>'
    batch_size = 12
    page = 1
    no_results_message = '<p>There are no upcoming events.</p>'

    def format_date(self, date):
        if date:
            date = self.translation_service.ulocalized_time(
                DateTime(date), True, False, self.context)
        return date

    def listings(self, b_start=None, b_size=None):
        """get a page of listings"""
        if b_size is None:
            b_size = self.batch_size
        if b_start is None:
            b_start = (getattr(self, 'page', 1) - 1) * b_size
        content_filter = {}
        is_collection = self.context.portal_type == 'Collection'
        if not is_collection:
            content_filter = {
                'portal_type': 'Event',
                'sort_on': 'start',
                'sort_order': 'ascending',
                'review_state': 'published',
            }
        text = self.request.get('SearchableText')
        if text:
            content_filter['SearchableText'] = text

        search_all = self.request.get('SearchAll')
        if search_all == 'yes':
            content_filter['start'] = {'query': DateTime('1900/01/01'),
                                       'range': 'min'}
        elif search_all == 'no' or not is_collection:
            content_filter['start'] = {'query': DateTime(), 'range': 'min'}

        start = self.request.get('start')
        if start:
            content_filter['start'] = start
        end = self.request.get('end')
        if end:
            content_filter['end'] = end
        if is_collection:
            batch = self.context.results(batch=True, b_start=b_start,
                                         b_size=b_size, brains=True,
                                         custom_query=content_filter)
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            items = catalog(**content_filter)
            batch = Batch(items, b_size, b_start)

        return batch

    def get_no_results_message(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IISAWSettings)
        return getattr(settings, 'no_results_message', self.no_results_message)
