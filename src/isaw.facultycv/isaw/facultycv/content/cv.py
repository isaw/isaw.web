"""Definition of the CV content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata
from zope.formlib import form

from isaw.facultycv.interfaces import ICV
from isaw.facultycv.config import PROJECTNAME

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
        name = 'Education and Degrees',
        widget = atapi.RichWidget(
            label=u'Education and Degrees',
            label_msgid='isaw.facultycv_label_Eddegrees',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Positions held',
        widget = atapi.RichWidget(
            label=u'Positions Held',
            label_msgid='isaw.facultycv_label_Positions',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Honors',
        widget = atapi.RichWidget(
            label=u'Academic Honors and Awards',
            label_msgid='isaw.facultycv_label_Honors',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Professional Offices and Service',
        widget = atapi.RichWidget(
            label=u'Professional Offices and Service',
            label_msgid='isaw.facultycv_label_ProfessionalOffices',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Research and works in progress',
        widget = atapi.RichWidget(
            label=u'Research',
            label_msgid='isaw.facultycv_label_Research',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Research Awards',
        widget = atapi.RichWidget(
            label = u'Research Awards',
            label_msgid = 'isaw.facultycv_label_ResearchAwards',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'List of Courses',
        widget = atapi.RichWidget(
            label = u'List of Courses taught',
            label_msgid = 'isaw.facultycv_label_CoursesTaught',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True

    ),

    atapi.TextField(
        name = 'Graduate Supervision',
        widget = atapi.RichWidget(
            label = u'Graduate Supervision',
            label_msgid = 'isaw.facultycv_label_GradSupervise',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),


    atapi.TextField(
        name = 'Publications',
        widget = atapi.RichWidget(
            label = u'Publications',
            label_msgid = 'isaw.facultycv_label_Publications',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Papers',
        widget = atapi.RichWidget(
            label = u'Papers',
            label_msgid = 'isaw.facultycv_label_Papers',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    ),

    atapi.TextField(
        name = 'Lectures',
        widget = atapi.RichWidget(
            label = u'Lectures',
            label_msgid = 'isaw.facultycv_label_Lectures',
            il8n_domain='isaw.facultycv',
            ),

        required = False,
        searchable = True
    )

    ### OK, so realistically this isn't supposed to work like this
    ### Unfortunately what I wanted to use (Zotero) lacks a useful API
    ### So the data stored here is explicit to a Plone instance
    ### Will update about this more later
    ### Christopher Warner - christopher.warner@nyu.edu

#   atapi.StringField(
#       name = 'Publication List',
#       widget = atapi.SelectionWidget(
#           label = u'Publications',
#           label_msgid = 'isaw.facultycv_label_TypeOfPublications',
#           il8n_domain='isaw.facultycv',
#           ),
#
#       required = False,
#       searchable = True
#   )


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
