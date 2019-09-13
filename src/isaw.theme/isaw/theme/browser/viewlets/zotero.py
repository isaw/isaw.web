from urlparse import urlparse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

ZOTERO_JSON_BASE = 'https://api.zotero.org{}?v=3&format=json'


class PublicationZoteroViewlet(ViewletBase):
    render = ViewPageTemplateFile('zotero.pt')
    html_ref = None
    json_ref = None

    def update(self):
        zotero_url = getattr(self.context, 'bibliographic_uri', None)
        if zotero_url and zotero_url.startswith('https://www.zotero.org/users/'):
            self.html_ref = zotero_url
            zotero_path = urlparse(zotero_url).path
            self.json_ref = ZOTERO_JSON_BASE.format(zotero_path)
