from Products.Five.browser import BrowserView


class PeopleView(BrowserView):
    """Base vew class for the @@people-view"""

    def people(self):
        brains = self._query()
        result = []
        for brain in brains:
            profile = brain.getObject()
            data = {
                'id': profile.getId(),
                'name': profile.Title(),
                'email': profile.Email or '',
                'html_blurb': profile.Titles(),
                'url': profile.absolute_url(),
                'has_image': getattr(profile, 'Image', False),
                'image_url': '{}/@@images/Image/mini'.format(
                    profile.absolute_url()
                ),
            }
            result.append(data)

        return result


class PeopleViewFolder(PeopleView):
    """View class for the @@people-view on Folders"""

    def _query(self):
        return self.context.getFolderContents(
            contentFilter={'portal_type': 'profile'}
        )


class PeopleViewCollection(PeopleView):
    """View class for the @@people-view on Collections"""

    def _query(self):
        return self.context.queryCatalog()
