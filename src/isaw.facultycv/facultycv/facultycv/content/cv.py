"""Definition of the CV content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from facultycv.facultycv.interfaces import ICV
from facultycv.facultycv.config import PROJECTNAME

CVSchema = folder.ATFolderSchema.copy() + atapi.Schema((

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

	atapi.LinesField(
		name = 'Education and Degrees',
		widget = atapi.LinesWidget(
			label=u'Education and Degrees',
			label_msgid='FacultyCV_label_Eddegrees',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'Positions held',
		widget = atapi.LinesWidget(
			label=u'Positions Held',
			label_msgid='FacultyCV_label_Positions',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'Honours',
		widget = atapi.LinesWidget(
			label=u'Honours',
			label_msgid='FacultyCV_label_Honours',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.LinesField(
		name= 'Professional Affiliations',
		widget = atapi.LinesWidget(
			label=u'Professional Affiliations',
			label_msgid='FacultyCV_label_ProfessionalAffiliations',
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

	atapi.LinesField(
		name = 'Research Awards',
		widget = atapi.LinesWidget(
			label = u'Research Awards',
			label_msgid = 'FacultyCV_label_ResearchAwards',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'List of Courses',
		widget = atapi.LinesWidget(
			label = u'List of Courses taught',
			label_msgid = 'FacultyCV_label_CoursesTaught',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True

	),

	atapi.LinesField(
		name = 'Graduate Supervsion',
		widget = atapi.LinesWidget(
			label = u'Graduate Supervision',
			label_msgid = 'FacultyCV_label_GradSupervise',
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
		name = 'Publication Type',
		widget = atapi.SelectionWidget(
			label = u'Type of Publication',
			label_msgid = 'FacultyCV_label_TypeOfPublications',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'Publications',
		widget = atapi.LinesWidget(
			label = u'Publications',
			label_msgid = 'FacultyCV_label_Publications',
			il8n_domain='FacultyCV',
			),
		
		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'Papers',
		widget = atapi.LinesWidget(
			label = u'Papers',
			label_msgid = 'FacultyCV_label_Papers',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	),

	atapi.LinesField(
		name = 'Lectures',
		widget = atapi.LinesWidget(
			label = u'Lectures',
			label_msgid = 'FacultyCV_label_Lectures',
			il8n_domain='FacultyCV',
			),

		required = False,
		searchable = True
	)


))

CVSchema['title'].storage = atapi.AnnotationStorage()
CVSchema['description'].storage = atapi.AnnotationStorage()

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

    def initializeArchetype(self, **kwargs):
        self.invokeFactory("profile", id="profile", title='profile', )

atapi.registerType(CV, PROJECTNAME)
