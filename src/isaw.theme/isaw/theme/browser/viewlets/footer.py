from Acquisition import aq_inner
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ..interfaces import IISAWSettings


class SiteFooter(ViewletBase):
    render = ViewPageTemplateFile('footer.pt')

    def html(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')
        user_actions = context_state.actions('user')
        actions_html = '<ul>'
        for action in user_actions:
            actions_html += '<li id="personaltools-{}">'.format(action['id'])
            actions_html += '<a href="{}">{}</a>'.format(action['url'],
                                                         action['title'])
            actions_html += '</li>'
        actions_html += '</ul>'
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IISAWSettings, False)
        html = getattr(settings, 'footer_html', u'')
        html = html.replace('<ul id="personal-tools-links"></ul>', actions_html)
        return html
