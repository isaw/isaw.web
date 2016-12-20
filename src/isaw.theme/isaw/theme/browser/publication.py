from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from isaw.bibitems.browser.view import BibItemView


class PublicationView(BibItemView):
    """view class"""

    @property
    def authors(self):
        members = self._get_members(self.context.authors)
        return ', '.join(members)

    @property
    def contributors(self):
        members = self._get_members(self.context.contributors)
        return ', '.join(members)

    @property
    def editors(self):
        members = self._get_members(self.context.editors)
        return ', '.join(members)

    def _get_members(self, member_list):
        mt = getToolByName(self.context, 'portal_membership')
        members = []
        for author in member_list:
            author = author.strip()
            if not author:
                continue
            info = mt.getMemberInfo(author)
            if info:
                members.append('<a href="%s">%s</a>' % (info.get('home_page'),
                               info.get('fullname', author)))
            else:
                members.append(author)
        return members

    @property
    def images(self):
        return self.context.objectValues()


class PublicationImagesView(BrowserView):
    """ images overlay """

    @property
    def images(self):
        return self.context.objectValues()
