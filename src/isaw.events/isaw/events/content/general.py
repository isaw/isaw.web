"""Definition of the events content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin

from isaw.events import IsawEventMessageFactory as _
from isaw.events.interfaces import IGeneral
from isaw.events.config import PROJECTNAME

GeneralSchema = folder.ATFolderSchema.copy() + atapi.Schema((

# -*- Events Schema -*- #
    atapi.ImageField(
    name='event_Image',
    widget=atapi.ImageWidget(
        label=u'Event Image',
        description=_(u'event_image', default=u'Optional image associated with the event.'),
        label_msgid='ISAW_Event_image',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),
   
    atapi.StringField(
    name='event_Image_caption',
    widget=atapi.TextAreaWidget(
        label=u'Event Image Caption',
        description=_(u'event_image_caption', default=u'Optional image caption associated with image.'),
        label_msgid='ISAW_Event_image_caption',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=False),

    atapi.TextField(
    name='event_Abstract',
    accessor='abstract',
    default_output_type='text/html',
    widget=atapi.RichWidget(
        label=u'Event Abstract',
        description=_(u'event_abstract', default=u'A summary statement of the description.'),
        label_msgid='ISAW_Event_abstract',
        il8n_domain='ISAW_Event',
        allow_file_upload=True,
        ),

    required=False,
    searchable=True),

    atapi.StringField(
    name='event_Speaker',
    accessor='speaker',
    widget=atapi.StringWidget(
        description=_(u'event_Speaker', default=u'The person speaking or holding the event.'),
        label=u'Event Speaker',
        label_msgid='ISAW_Event_Speaker',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),

    atapi.TextField(
    name='event_Speaker_detail',
    widget=atapi.TextAreaWidget(
        label=u'Event Speaker Detail',
        description=_(u'event_speaker_detail', default=u'Background of the speaker.'),
        label_msgid='ISAW_Event_Speaker_detail',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    # Organizers/Contributors
    
#    atapi.StringField(
#    name='event_Location',
    # I don't like the dependence on this widget
    # will think about either extending DynamicSelectWidget
    # or releasing a new version of it
#    widget=atapi.StringWidget(
#        label=u'Event Location',
#        label_msgid='ISAW_Event_location',
#        il8n_domain='ISAW_Event',
#        maxlength=255,
#        size=50,
#        ),
        
#    vocabulary=DisplayList((
#    ('Library', u'Oak Library'),
#    ('Lecture', u'Lecture Hall'),
#    ('Seminar', u'Seminar Room'),
#    ('Gallery 1', u'Gallery 1'),
#    ('Gallery 2', u'Gallery 2'),
#    ('Lunch', u'Lunch Room (basement)'),
#    ('Garden', u'Garden')
#    )),
    
#    required=False,
#    searchable=True),

    atapi.DateTimeField(
    name='event_StartDateTime',
    accessor='start',
    widget=atapi.CalendarWidget(
        description=_(u'event_startdatetime', default=u'The date and/or time when the event starts.'),
        label=u'Event Start Date and Time',
        label_msgid='ISAW_Event_StartDateTime',
        il8n_domain='ISAW_Event',
        show_hm=True,
        format="%A, %B %d %Y %X %p %z",
        ),

    required=True,
    searchable=True),

    atapi.DateTimeField(
    name='event_EndDateTime',
    accessor='end',
    widget=atapi.CalendarWidget(
        description=_(u'event_enddatetime', default=u'The date and/or time when the event ends.'),
        label=u'Event End Date and Time',
        label_msgid='ISAW_Event_EndDateTime',
        il8n_domain='ISAW_Event',
        show_hm=True,
        format='%A, %B %d %Y %X %p %z'
        ),

    required=True,
    searchable=True),


#    atapi.LinesField(
#    name='event_Type',
#    vocabulary = DisplayList((
#        ('lecture', 'An event lecture'),
#        ('conference', 'An event conference'),
#        ('film', 'An event where a film will be shown'),
#        ('concert', 'An event where a concert will be held'),
#        )),
#        
#        widget=atapi.PicklistWidget(
#        label=u'What type of Event is this?',
#        label_msgid='ISAW_Event_Type',
#        il8n_domain='ISAW_Event',
#        ),
#        
#    required=False,
#    searchable=True),
    
    atapi.BooleanField(
    name='event_Private',
    schemata='options',
    widget=atapi.BooleanWidget(
        description=_(u'event_private', default=u'If selected, only ISAW faculty/admin/staff will be able to view this event.'),
        label=u'Private Event',
        label_msgid='ISAW_Event_Private',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),

    atapi.BooleanField(
    name='event_Reception',
    schemata='options',
    widget=atapi.BooleanWidget(
        description=_(u'event_reception', default=u'If selected, the event will have a reception following.'),
        label=u'Reception',
        label_msgid='ISAW_Event_reception',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),
    
    atapi.BooleanField(
    name='event_Rsvp',
    schemata='options',
    widget=atapi.BooleanWidget(
        label=u'RSVP for this event?',
        description=_(u'event_rsvp', default=u'If selected, one will need to RSVP for this event the default address is isaw@nyu.edu.'),
        label_msgid='ISAW_Event_rsvp',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),

    atapi.StringField(
    name='event_custom_Rsvp',
    schemata='options',
    validators= ('isEmail'),
    widget=atapi.StringWidget(
        label=u'RSVP email address',
        description=_(u'event_custom_rsvp', default=u'RSVP contact email, default is isaw@nyu.edu'),
        label_msgid='ISAW_Event_custom_rsvp',
        il8n_domain='ISAW_Event',
        ),
   
    required=False,
    searchable=True),
 
    # After about 10 minutes deliberation
    # instead of making this an Annotation i've added it to the object itself
    # the reason being is all data should be stored/managed in the object if it's small enough
    
    atapi.IntegerField(
    name='event_BlogId',
    widget=atapi.IntegerWidget(
        label=u'Event Blog id',
        label_msgid='ISAW_Event_blogid',
        il8n_domain='ISAW_Event',
        size=10,
        visible={'view': 'visible', 
                'edit': 'hidden'},
        ),
    
    # Does isMetadata work anymore?
    isMetadata=True,
    required=False),
    

    atapi.BooleanField(
    schemata='options',
    name='event_Twitter',
    widget=atapi.BooleanWidget(
        description=_(u'event_twitter', default=u'If selected, this event will appear on Twitter @ http://twitter.com/isawnyu'),
        label=u'Post this event on Twitter?',
        label_msgid='ISAW_Event_twitter',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
#    atapi.BooleanField(
#    schemata='options',
#    name='event_Facebook',
#    widget=atapi.BooleanWidget(
#        description=_(u'event_facebook', default=u'If selected, this event will appear on Facebook.'),
#        label=u'Post this event on Facebook?',
#        label_msgid='ISAW_Event_facebook',
#        il8n_domain='ISAW_Event',
#        ),
#
#    required=False,
#    searchable=True),

    atapi.BooleanField(
    schemata='options',
    name='event_Blog',
    widget=atapi.BooleanWidget(
        description=_(u'event_blog', default=u'If selected, this event will appear on the news blog.'),
        label=u'Post this event on the news blog?',
        label_msgid='ISAW_Event_blog',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.BooleanField(
    schemata='options',
    name='event_Invite',
    widget=atapi.BooleanWidget(
        description=_(u'event_invite', default=u'If selected, this event will be invitation only.'),
        label=u'Invitation only',
        label_msgid='ISAW_Event_isaw',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.IntegerField(
    name='event_TwitterId',
    widget=atapi.IntegerWidget(
        label=u'Event Twitter id',
        label_msgid='ISAW_Event_twitterid',
        il8n_domain='ISAW_Event',
        size=10,
        visible={'view': 'visible', 
                'edit': 'hidden'},
        ),
    
    # Does isMetadata work anymore?
    isMetadata=True,
    required=False),

    atapi.StringField(
        name='event_Url',
        required=False,
        searchable=True,
        accessor='event_url',
        validators=('isURL',),
        widget = atapi.StringWidget(
            description = _(u'help_event_url',
                default=u"Web address with more info about the event. "
                "Add http:// for external links."),
                label = _(u'label_event_url', default=u'Event URL')
             )),

    atapi.StringField(
        name='contactName',
        required=False,
        searchable=True,
        accessor='contact_name',
        widget = atapi.StringWidget(
            description = '', 
                label = _(u'label_contact_name', default=u'Contact Name')
        )), 

    atapi.StringField('contactEmail',
        required=False,
        searchable=True,
        accessor='contact_email',
        validators = ('isEmail',),
        widget = atapi.StringWidget(
            description = '', 
                label = _(u'label_contact_email', default=u'Contact E-mail')
        )), 

    atapi.StringField('contactPhone',
        required=False,
        searchable=True,
        accessor='contact_phone',
        validators= (), 
        widget = atapi.StringWidget(
            description = '', 
                label = _(u'label_contact_phone', default=u'Contact Phone')
        )), 

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

GeneralSchema['title'].storage = atapi.AnnotationStorage()
GeneralSchema['description'].storage = atapi.AnnotationStorage()

#override finalizeATCTSchema
def finalizeATCTSchema(schema, folderish=False, moveDiscussion=True):
    """Finalizes an ATCT type schema to alter some fields
       for the event type. This had to be overrided - cwarner
    """
    schema.moveField('relatedItems', pos='bottom')
    if folderish:
        schema['relatedItems'].widget.visible['edit'] = 'invisible'
    schema.moveField('excludeFromNav', after='allowDiscussion')
    if moveDiscussion:
        schema.moveField('allowDiscussion', after='relatedItems')

    schema.moveField('event_Image', after='title')
    schema.moveField('event_Image_caption', after='event_Image')

    # Categorization
    if schema.has_key('subject'):
        schema.changeSchemataForField('subject', 'tags')
    if schema.has_key('relatedItems'):
        schema.changeSchemataForField('relatedItems', 'tags')
    if schema.has_key('location'):
        schema.changeSchemataForField('location', 'default')
        schema.moveField('location', after='event_Speaker')
    if schema.has_key('language'):
        schema.changeSchemataForField('language', 'default')

    # Dates
    if schema.has_key('effectiveDate'):
        schema.changeSchemataForField('effectiveDate', 'default')
        schema.moveField('effectiveDate', after='event_EndDateTime')
    if schema.has_key('expirationDate'):
        schema.changeSchemataForField('expirationDate', 'default')    
        schema.moveField('expirationDate', after='effectiveDate')
    if schema.has_key('creation_date'):
        schema.changeSchemataForField('creation_date', 'dates')    
    if schema.has_key('modification_date'):
        schema.changeSchemataForField('modification_date', 'dates')    

    # Ownership
    if schema.has_key('creators'):
        schema.changeSchemataForField('creators', 'organizers')
    if schema.has_key('contributors'):
        schema.changeSchemataForField('contributors', 'organizers')
    if schema.has_key('rights'):
        schema.changeSchemataForField('rights', 'organizers')

    # Settings
    if schema.has_key('allowDiscussion'):
        schema.changeSchemataForField('allowDiscussion', 'options')
    if schema.has_key('excludeFromNav'):
        schema.changeSchemataForField('excludeFromNav', 'options')
    if schema.has_key('nextPreviousEnabled'):
        schema.changeSchemataForField('nextPreviousEnabled', 'options')

    schemata.marshall_register(schema)
    return schema

finalizeATCTSchema(
    GeneralSchema,
    folderish=True,
    moveDiscussion=False
)

class General(folder.ATFolder, CalendarSupportMixin):
    """Isaw Events Module"""
    implements(IGeneral)

    meta_type = "General Event"
    schema = GeneralSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(General, PROJECTNAME)
