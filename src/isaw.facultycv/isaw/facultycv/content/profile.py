"""Definition of the profile content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import ImageField

from isaw.facultycv.interfaces import Iprofile
from isaw.facultycv.config import PROJECTNAME

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
# it is initally set at creation of a new CV
# Description is null, realistically it's not needed but I may add some default stock

profileSchema['title'].required = 0
profileSchema['title'].widget.visible = {"edit": "invisible"}
profileSchema['description'].widget.visible = {"edit": "invisible"}

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

atapi.registerType(profile, PROJECTNAME)
