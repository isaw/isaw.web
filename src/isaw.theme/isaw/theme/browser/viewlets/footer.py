from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ..interfaces import IISAWSettings


class SiteFooter(ViewletBase):
    render = ViewPageTemplateFile('footer.pt')

    def html(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IISAWSettings, False)
        html = getattr(settings, 'footer_html', u'')
        return html
