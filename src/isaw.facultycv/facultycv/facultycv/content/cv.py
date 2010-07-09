"""Definition of the CV content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from facultycv.facultycv.interfaces import ICV
from facultycv.facultycv.config import PROJECTNAME
from Products.ATContentTypes import ATCTMessageFactory as _

CVSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.ReferenceField(
        name = 'ProfileRef',

        widget = atapi.ReferenceWidget(
            label = u'Profile reference',
        ),
        relationship = 'owned_profile',
        multiValued=False,
    ),


	atapi.TextField(
		name = 'Address',
		widget = atapi.RichWidget(
			label=u'Address',
			label_msgid='FacultyCV_label_Address',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.StringField(
		name = 'Email',
		widget = atapi.StringWidget(
			label=u'Email Address',
			label_msgid='FacultyCV_label_Email',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.StringField(
		name = 'Phone',
		widget = atapi.StringWidget(
			label=u'Phone number',
			label_msgid='FacultyCV_label_Phone',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Education and Degrees',
		widget = atapi.RichWidget(
			label=u'Education and Degrees',
			label_msgid='FacultyCV_label_Eddegrees',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Positions held',
		widget = atapi.RichWidget(
			label=u'Positions Held',
			label_msgid='FacultyCV_label_Positions',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Honors',
		widget = atapi.RichWidget(
			label=u'Academic Honors and Awards',
			label_msgid='FacultyCV_label_Honors',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.TextField(
		name= 'Professional Affiliations',
		widget = atapi.RichWidget(
			label=u'Professional Affiliations',
			label_msgid='FacultyCV_label_ProfessionalAffiliations',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),


	atapi.TextField(
		name = 'Professional Offices and Service',
		widget = atapi.RichWidget(
			label=u'Professional Offices and Service',
			label_msgid='FacultyCV_label_ProfessionalOffices',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Research and works in progress',
		widget = atapi.RichWidget(
			label=u'Research',
			label_msgid='FacultyCV_label_Research',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Research Awards',
		widget = atapi.RichWidget(
			label = u'Research Awards',
			label_msgid = 'FacultyCV_label_ResearchAwards',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'List of Courses',
		widget = atapi.RichWidget(
			label = u'List of Courses taught',
			label_msgid = 'FacultyCV_label_CoursesTaught',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True

	),

	atapi.TextField(
		name = 'Graduate Supervision',
		widget = atapi.RichWidget(
			label = u'Graduate Supervision',
			label_msgid = 'FacultyCV_label_GradSupervise',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),


	atapi.TextField(
		name = 'Publications',
		widget = atapi.RichWidget(
			label = u'Publications',
			label_msgid = 'FacultyCV_label_Publications',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Papers',
		widget = atapi.RichWidget(
			label = u'Papers',
			label_msgid = 'FacultyCV_label_Papers',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.TextField(
		name = 'Lectures',
		widget = atapi.RichWidget(
			label = u'Lectures',
			label_msgid = 'FacultyCV_label_Lectures',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	### OK, so realistically this isn't supposed to work like this
	### Unfortunately what I wanted to use (Zotero) lacks a useful API
	### So the data stored here is explicit to a Plone instance
	### Will update about this more later
	### Christopher Warner - christopher.warner@nyu.edu 

	atapi.StringField(
		name = 'Publication List',
		widget = atapi.SelectionWidget(
			label = u'Publications',
			label_msgid = 'FacultyCV_label_TypeOfPublications',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	)


))

CVSchema['title'].storage = atapi.AnnotationStorage()
CVSchema['description'].storage = atapi.AnnotationStorage()

# We don't need to show the reference field
CVSchema['ProfileRef'].widget.visible = {"edit": "invisible",
										 "view": "invisible"}

schemata.finalizeATCTSchema(
    CVSchema,
    folderish=True,
    moveDiscussion=False
)


class CV(folder.ATFolder):
    """CV of Faculty Member"""
    implements(ICV)

    meta_type = "CV"
    schema = CVSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(CV, PROJECTNAME)
