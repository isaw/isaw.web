"""Definition of the profile content type
"""

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
        name='ProfileRef',

        widget=atapi.ReferenceWidget(
            label=u'Profile reference',
        ),
        relationship='owned_profile',
        multiValued=False,
    ),

    atapi.TextField(
        name='Titles',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=u'Faculty Titles',
            label_msgid='isaw.facultycv_label_Titles',
            il8n_domain='isaw.facultycv',
        ),

        required=False,
        searchable=True
    ),

    atapi.StringField(
        name='Phone',
        default_output_type='text/x-html-safe',
        widget=atapi.StringWidget(
            label=u'Phone',
            label_msgid='isaw.facultycv_label_Phone',
            il8n_domain='isaw.facultycv',
        ),

        required=False,
        searchable=True

    ),

    atapi.StringField(
        name='Email',
        default_output_type='text/x-html-safe',
        widget=atapi.StringWidget(
            label=u'Email',
            label_msgid='isaw.facultycv_label_Email',
            il8n_domain='isaw.facultycv',
        ),

        required=False,
        searchable=True

    ),

    atapi.StringField(
        name='Address',
        default_output_type='text/x-html-safe',
        widget=atapi.StringWidget(
            label=u'Address Information',
            label_msgid='isaw.facultycv_label_Address',
            il8n_domain='isaw.facultycv',
        ),

        required=False,
        searchable=True

    ),

    atapi.TextField(
        name='Profile Blurb',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=u'Profile Blurb',
            label_msgid='isaw.facultycv_label_Profile',
            il8n_domain='isaw.facultycv',
        ),

        required=False,
        searchable=True
    ),


    atapi.StringField(
        name='MemberID',
        vocabulary_factory="isaw.facultycv.Users",
        enforceVocabulary=True,
        widget=atapi.SelectionWidget(
            label=u'Associated Member ID',
            label_msgid='isaw.facultycv_label_MemberID',
            il8n_domain='isaw.facultycv',
        ),
        required=False,
    ),

))

profileSchema['title'].storage = atapi.AnnotationStorage()
profileSchema['description'].storage = atapi.AnnotationStorage()

profileSchema['description'].widget.visible = {"edit": "invisible"}
profileSchema['ProfileRef'].widget.visible = {"edit": "invisible"}


schemata.finalizeATCTSchema(
    profileSchema,
    folderish=True,
    moveDiscussion=False
)


class profile(folder.ATFolder):
    """Profile"""
    implements(Iprofile)

    meta_type = "Profile"
    schema = profileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(profile, PROJECTNAME)
