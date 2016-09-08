from Products.Five.browser import BrowserView
from zope.interface import implements

from isaw.theme.browser.interfaces import IBibliographicListingView


class BibliographicListingView(BrowserView):
    """view class"""
    implements(IBibliographicListingView)
    batch_size = 0
    page = 1

    def __init__(self, request, context):
        super(BibliographicListingView, self).__init__(request, context)
        self.page = int(self.request.get('page', 1))

    def _query(self, query=None, exclude=None, b_start=None, b_size=None):
        if b_size is None:
            b_size = self.batch_size
        if b_start is None:
            b_start = (getattr(self, 'page', 1) - 1) * b_size

        if query is None:
            query = {}

        if exclude is not None:
            uuid = getattr(exclude, 'UID')
            if callable(uuid):
                uuid = uuid()
            if uuid:
                query['UID'] = {'not': uuid}

        if self.context.portal_type == 'Folder':
            self.request['b_start'] = b_start
            self.request['b_size'] = b_size
            query['b_start'] = b_start
            query['b_size'] = b_size
            items = self.context.getFolderContents(contentFilter=query,
                                                   batch=True, b_size=b_size)
        elif self.context.portal_type == 'Topic':
            if b_start and not self.request.get('b_start'):
                self.request['b_start'] = b_start
            items = self.context.queryCatalog(self.request, True, b_size,
                                              **query)
        elif self.context.portal_type == 'Collection':
            items = self.context.results(True, b_start, b_size,
                                         custom_query=query)
        else:
            items = []

        return items

    def listings(self, b_start=None, b_size=None):
        """get a page of listings"""
        return self._query(b_start=b_start, b_size=b_size)
