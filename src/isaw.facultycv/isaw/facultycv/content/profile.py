"""Definition of the profile content type
"""

from urlparse import urlparse
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from isaw.facultycv.interfaces import Iprofile
from isaw.facultycv.config import PROJECTNAME

profileSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.ImageField(
        name='Image',
        sizes=None,
        widget=atapi.ImageWidget(
            label=u'Profile Image',
            label_msgid='isaw.facultycv_label_ProfileImage',
            il8n_domain='isaw.facultycv',
        ),
        required=False,
        searchable=True,
        accessor='profileImage',
    ),

    atapi.ReferenceField(
        name = 'ProfileRef',

        widget = atapi.ReferenceWidget(
            label = u'Profile reference',
        ),
        relationship = 'owned_profile',
        multiValued=False,
    ),

    atapi.TextField(
        name = 'Titles',
        default_output_type='text/x-html-safe',
        widget = atapi.RichWidget(
            label=u'Faculty Titles',
            label_msgid='isaw.facultycv_label_Titles',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.StringField(
        name = 'Phone',
        default_output_type='text/x-html-safe',
        widget = atapi.StringWidget(
            label=u'Phone',
            label_msgid='isaw.facultycv_label_Phone',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True

    ),

    atapi.StringField(
        name = 'Email',
        default_output_type='text/x-html-safe',
        widget = atapi.StringWidget(
            label=u'Email',
            label_msgid='isaw.facultycv_label_Email',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True

    ),

    atapi.StringField(
        name = 'Address',
        default_output_type='text/x-html-safe',
        widget = atapi.StringWidget(
            label=u'Address Information',
            label_msgid='isaw.facultycv_label_Address',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True

    ),

    atapi.TextField(
        name = 'Profile Blurb',
        default_output_type='text/x-html-safe',
        widget = atapi.RichWidget(
            label=u'Profile Blurb',
            label_msgid='isaw.facultycv_label_Profile',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.LinesField(
        name='ExternalURIs',
        required=False,
        widget=atapi.LinesWidget(
            label=u'External URIs (e.g. VIAF, Facebook, GitHub, etc.)',
            label_msgid='isaw.facultycv_label_external_uris',
            il8n_domain='isaw.facultycv',
        ),
    ),

))

profileSchema['title'].storage = atapi.AnnotationStorage()
profileSchema['description'].storage = atapi.AnnotationStorage()

# We hide the Title because it isn't needed or required even though
# it is initally set at creation of a new CV and not a profile itself
# Description is null, realistically it's not needed but I may add some default stock
# in the future

#profileSchema['title'].required = 0
#profileSchema['title'].widget.visible = {"edit": "invisible",
#                                        "view": "invisible"}
profileSchema['description'].widget.visible = {"edit": "invisible"}
profileSchema['ProfileRef'].widget.visible = {"edit": "invisible"}


schemata.finalizeATCTSchema(
    profileSchema,
    folderish=True,
    moveDiscussion=False
)


DOMAIN_LINK_MAP = {
    'facebook.com': {
        "icon": "facebook-official",
        "title": "{fullname}'s facebook profile"
    },
    'academia.edu': {
        "icon": "university",
        "title": "{fullname}'s profile on academia.edu"
    },
    'github.com': {
        "icon": "github",
        "title": "{fullname}'s github profile"
    },
    'plus.google.com': {
        "icon": "google-plus-official",
        "title": "{fullname}'s google plus page"
    },
    'linkedin.com': {
        "icon": "linkedin-square",
        "title": "{fullname}'s linkedin profile"
    },
    'orcid.org': {
        "icon": "id-card-o",
        "title": "{fullname}'s orcid profile"
    },
    'twitter.com': {
        "icon": "twitter-square",
        "title": "{fullname}'s twitter profile"
    },
    'viaf.org': {
        "icon": "tags",
        "title": "{fullname}'s viaf id"
    },
    'wikipedia.org': {
        "icon": "wikipedia-w",
        "title": "{fullname}'s wikipedia user profile",
        "path": "/wiki/User"
    },
    'zotero.org': {
        "icon": "book",
        "title": "{fullname}'s zotero library"
    },
}


class profile(folder.ATFolder):
    """Profile"""
    implements(Iprofile)

    meta_type = "Profile"
    schema = profileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def profile_links(self):
        links = self.getExternalURIs() or []
        results = []
        for link in links:
            parts = urlparse(link)
            for link_id in DOMAIN_LINK_MAP:
                if not parts.hostname.endswith(link_id):
                    continue
                info = DOMAIN_LINK_MAP[link_id].copy()
                if (info.get('path') and not
                        parts.path.startswith(info['path'])):
                    continue
                info["title"] = info["title"].format(fullname=self.Title())
                info["link"] = link
                results.append(info)
        return results

atapi.registerType(profile, PROJECTNAME)
