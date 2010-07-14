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
	    sizes = { 'profile': (250,250),
				  'big': (600,600) },
		widget = atapi.ImageWidget(
			label = u'Profile Image',
			label_msgid='FacultyC_label_ProfileImage',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True

	),

	atapi.TextField(
		name = 'Profile Blurb',
		widget = atapi.RichWidget(
			label=u'Short Profile Blurb',
			label_msgid='FacultyCV_label_Profile',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	)

))

profileSchema['title'].storage = atapi.AnnotationStorage()
profileSchema['description'].storage = atapi.AnnotationStorage()

# We hide the Title because it isn't needed or required even though
# it is initally set at creation of a new CV and not a profile itself
# Description is null, realistically it's not needed but I may add some default stock
# in the future

profileSchema['title'].required = 0
profileSchema['title'].widget.visible = {"edit": "invisible",
										 "view": "invisible"}
profileSchema['description'].widget.visible = {"edit": "invisible"}

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
