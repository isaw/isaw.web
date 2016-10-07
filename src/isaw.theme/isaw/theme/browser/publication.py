from Products.CMFCore.utils import getToolByName

from isaw.bibitems.browser.view import BibItemView


class PublicationView(BibItemView):
    """view class"""

    @property
    def byline(self):
        by = ''
        if self.context.authors:
            by += 'By: '
            members = self._get_members(self.context.authors)
            by += ', '.join(members)
        if self.context.contributors:
            by += ', with contributions from '
            members = self._get_members(self.context.contributors)
            by += ', '.join(members)
        by += '.'
        return by

    def _get_members(self, member_list):
        mt = getToolByName(self.context, 'portal_membership')
        members = []
        for author in member_list:
            info = mt.getMemberInfo(author)
            if info:
                members.append('<a href="%s">%s</a>' % (info.get('home_page'),
                               info.get('fullname', author)))
            else:
                members.append(author)
        return members
