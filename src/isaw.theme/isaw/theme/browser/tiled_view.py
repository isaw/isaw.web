# -*- coding: utf-8 -*-
"""View providing a tiled layout for listed items

Suitable for folders or collections
"""
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from isaw.theme.browser.interfaces import ITiledListingView


class TiledListingView(BrowserView):
    """view class"""
    implements(ITiledListingView)

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

    def listings(self, batch=True, b_start=1, b_size=9, sort_on=None, **kwargs):
        """get a page of listings"""
        if self.context.portal_type == 'Folder':
            content_filter = {
                'sort_on': sort_on,
                'b_start': b_start,
                'b_size': b_size,
            }
            content_filter.update(kwargs)
            items = self.context.getFolderContents(
                content_filter, batch=batch
            )
        elif self.context.portal_type == 'Topic':
            if sort_on:
                kwargs['sort_on'] = sort_on
            # topics look for b_start on the request
            if b_start and not self.request.get('b_start'):
                self.request['b_start'] = b_start
            items = self.context.queryCatalog(
                self.request, batch, b_size, **kwargs
            )
        elif self.context.portal_type == 'Collection':
            items = self.context.results(
                batch, b_start, b_size, sort_on, **kwargs
            )
        else:
            items = []
        return items

    def first_item(self):
        """get the 'first item' for the listing

        Once implemented, this should return the 'sticky' item for this
        context, or the first item in the listing if the sticky item is not in
        the listing or is not set.
        """
        batch = self.listings(batch=True, b_start=0, b_size=1, sort_on=None)
        return [i for i in batch][0]

    def get_byline(self, brain):
        author_info = self.membership_tool.getMemberInfo(brain.Creator)
        author = author_info.get('fullname') or author_info.get('username') or brain.Creator
        parts = [author]
        date = brain.EffectiveDate
        if date:
            parts.append(DateTime(date).strftime("%d/%m/%Y"))
        return "by " + " | ".join(parts)

    def get_image(self, brain):
        scales = self.context.restrictedTraverse(brain.getPath() + '/@@images')
        try:
            scale = scales.scale('image', 'blogtile')
            return '<img src={} title={} />'.format(scale.url, brain.Title)
        except (TypeError, AttributeError):
            # no image available, use the placeholder div
            return '<div class="img_placeholder">&nbsp;</div>'
