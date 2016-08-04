from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner, aq_parent
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName
from plone.app.layout.nextprevious.view import (NextPreviousView,
                                                NextPreviousViewlet,
                                                NextPreviousLinksViewlet)


class HighlightsNextPreviousView(NextPreviousView):

    def __init__(self, context, request=None, view=None, manager=None):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        props = getToolByName(context, 'portal_properties').site_properties
        self.vat = props.getProperty('typesUseViewActionInListings', ())
        self.security = getSecurityManager()
        order = aq_parent(aq_inner(context)).getOrdering()
        if not isinstance(order, list):
            order = order.idsInOrder()
        if not isinstance(order, list):
            order = None
        self.order = order

    def is_highlight(self, obj=None):
        if obj is None:
            obj = self.context
        if not callable(getattr(aq_base(obj), 'Subject', None)):
            return False
        if 'highlight' in obj.Subject():
            return True
        return False

    def getNextItem(self):
        """ return info about the next item in the container """
        obj = self.context
        parent = aq_parent(aq_inner(obj))
        if not self.order:
            return None
        order = list(self.order)
        pos = order.index(obj.getId())
        for oid in self.order[pos+1:]:
            data = self.getData(parent[oid])
            if data:
                return data

    def getPreviousItem(self):
        """ return info about the previous item in the container """
        obj = self.context
        parent = aq_parent(aq_inner(obj))
        if not self.order:
            return None
        order_reversed = list(reversed(self.order))
        pos = order_reversed.index(obj.getId())
        for oid in order_reversed[pos+1:]:
            data = self.getData(parent[oid])
            if data:
                return data

    def getData(self, obj):
        """ return the expected mapping, see `INextPreviousProvider` """
        if not self.security.checkPermission('View', obj):
            return None
        elif not IContentish.providedBy(obj):
            # do not return a not contentish object
            # such as a local workflow policy for example (#11234)
            return None
        elif not self.is_highlight(obj):
            return None

        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:       # "use view action in listings"
            url += '/view'
        return dict(
            id=obj.getId(),
            url=url,
            title=obj.Title(),
            description=obj.Description(),
            portal_type=ptype
        )

    def enabled(self):
        if self.is_highlight():
            return True
        return super(HighlightsNextPreviousView, self).enabled()

    def next(self):
        if self.is_highlight():
            return self.getNextItem()
        return super(HighlightsNextPreviousView, self).next()

    def previous(self):
        if self.is_highlight():
            return self.getPreviousItem()
        return super(HighlightsNextPreviousView, self).previous()


class HighlightsNextPreviousViewlet(HighlightsNextPreviousView,
                                    NextPreviousViewlet):
    pass


class HighlightsNextPreviousLinksViewlet(HighlightsNextPreviousView,
                                         NextPreviousLinksViewlet):
    pass
