# -*- coding: utf-8 -*-
"""View providing a tiled layout for listed items

Suitable for folders or collections

Also includes a viewlet which will show the "featured_item" returned by 
the method on the view.
"""
from DateTime import DateTime
from plone.app.layout.viewlets import common as base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from isaw.theme.browser.interfaces import ITiledListingView


class TileDetailsMixin(object):

    _translation_service = None
    _membership_tool = None

    @property
    def translation_service(self):
        if self._translation_service is None:
            self._translation_service = getToolByName(
                self.context, 'translation_service'
            )
        return self._translation_service

    @property
    def membership_tool(self):
        if self._membership_tool is None:
            self._membership_tool = getToolByName(
                self.context, 'portal_membership'
            )
        return self._membership_tool

    def get_byline(self, brain):
        author_info = self.membership_tool.getMemberInfo(brain.Creator)
        author = ''
        if author_info:
            author = author_info.get('fullname') or author_info.get('username')
        if author == '':
            author = brain.Creator
        parts = [author]
        date = brain.EffectiveDate
        if date:
            parts.append(DateTime(date).strftime("%d/%m/%Y"))
        return "by " + " | ".join(parts)

    def get_image(self, brain):
        scales = self.context.restrictedTraverse(brain.getPath() + '/@@images')
        try:
            scale = scales.scale('image', self.image_scale)
            return '<img src={} alt={} />'.format(scale.url, brain.Title)
        except (TypeError, AttributeError):
            # no image available, use the placeholder div
            return self.image_placeholder



class TiledListingView(BrowserView, TileDetailsMixin):
    """view class"""
    implements(ITiledListingView)
    image_scale = 'blogtile'
    image_placeholder = '<div class="blogtile_placeholder">&nbsp;</div>'
    batch_size = 9
    page = 1

    def __init__(self, request, context):
        super(TiledListingView, self).__init__(request, context)
        self.page = int(self.request.get('page', 1))

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

    def featured_item(self):
        """get the 'featured item' for the listing

        At this point, this is always the first item in the listing.

        Once implemented, this should return the 'sticky' item for this
        context, or the first item in the listing if the sticky item is not in
        the listing or is not set.
        """
        batch = self.listings(b_start=0, b_size=1)
        return [i for i in batch][0]


class FeaturedItemViewlet(base.ViewletBase, TileDetailsMixin):
    index = ViewPageTemplateFile('templates/featured_item.pt')
    image_scale = 'featured'
    image_placeholder = '<div class="featured_placeholder">&nbsp;</div>'

    def update(self):
        self.show = ITiledListingView.providedBy(self.view)

    def get_item(self):
        return self.view.featured_item()
