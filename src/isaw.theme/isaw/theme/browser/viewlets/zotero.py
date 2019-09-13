import re
from urlparse import urlparse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

ZOTERO_JSON_BASE = 'https://api.zotero.org{}?v=3&format=json'
Z_MATCH = re.compile(r'^/(groups|users)/\d+/items/[A-Z1-9]+$')


class PublicationZoteroViewlet(ViewletBase):
    render = ViewPageTemplateFile('zotero.pt')
    html_ref = None
    json_ref = None

    def update(self):
        zotero_url = getattr(self.context, 'bibliographic_uri', None)
        if not zotero_url:
            return
        parsed = urlparse(zotero_url)
        zotero_path = parsed.path
        domain = parsed.netloc
        if domain == 'www.zotero.org' and Z_MATCH.match(zotero_path):
            self.html_ref = zotero_url
            self.json_ref = ZOTERO_JSON_BASE.format(zotero_path)
