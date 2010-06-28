"""Definition of the profile content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import ImageField

from facultycv.facultycv.interfaces import Iprofile
from facultycv.facultycv.config import PROJECTNAME

profileSchema = folder.ATFolderSchema.copy() + atapi.Schema((

	atapi.ImageField(
		name = 'Image',
		widget = atapi.ImageWidget(
			label = u'Faculty Image',
			label_msgid='FacultyC_label_ProfileImage',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True

	),

	atapi.TextField(
		name = 'Profile',
		widget = atapi.RichWidget(
			label=u'Faculty Profile',
			label_msgid='FacultyCV_label_Profile',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.ReferenceField(
		name = 'cvref',
		relationship = 'OwnedBy',

		required = False,
		searchable = True
	)

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

profileSchema['title'].storage = atapi.AnnotationStorage()
profileSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    profileSchema,
    folderish=True,
    moveDiscussion=False
)


class profile(folder.ATFolder):
    """Faculty Profile"""
    implements(Iprofile)

    meta_type = "profile"
    schema = profileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(profile, PROJECTNAME)
