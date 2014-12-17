from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType


def copy_generic_fields(event):
    event_object = event.getObject()
    temp_id = "temp_copy_of_%s" % event_object.id
    container = aq_parent(event_object)
    _createObjectByType('Event', container, id=temp_id, title=event_object.title)
    new_event = container[temp_id]
    new_event.subtitle = event_object.subtitle()
    image_field = new_event.getField('leadImage')
    image_field.getMutator(new_event)(event_object.getEvent_Image())
    image_caption_field = new_event.getField('leadImage_caption')
    image_caption_field.getMutator(new_event)(event_object.getEvent_Image_caption())
    new_event.speaker = event_object.speaker()
    new_event.startDate = event_object.start()
    new_event.endDate = event_object.end()
    new_event.rsvpRequired = event_object.getEvent_Rsvp()
    new_event.contactName = event_object.contact_name()
    new_event.contactEmail = event_object.contact_email()
    new_event.contactPhone = event_object.contact_phone()
    new_event.location = event_object.getLocation()
    text = event_object.abstract()
    text += event_object.event_Speaker_detail()
    if event_object.event_Reception:
        text += "<p>There will be a reception folowing the event.</p>"
    if event_object.getEvent_Public():
        text += "<p>This is a public event.</p>"
    if event_object.event_custom_Rsvp:
        text += "<p>To RSVP, please email %s.</p>" % event_object.event_custom_Rsvp.encode('utf-8')
    else:
        text += "<p>To RSVP, please email isaw@nyu.edu.</p>"
    if event_object.event_Invite:
        text += "<p>This is an invitation only event.</p>"
    new_event.setText(text)
    return new_event

def remove_and_rename(event):
    event_id = event.getId
    temp_id = "temp_copy_of_%s" % event_id
    event_object = event.getObject()
    container = aq_parent(event_object)
    container.manage_delObjects([event_id])
    container.manage_renameObject(temp_id, event_id)
    

def migrate_events(context):
    properties = getToolByName(context, 'portal_properties')
    old_check = properties.site_properties.getProperty('enable_link_integrity_checks', False)
    properties.site_properties.enable_link_integrity_checks = False
    catalog = getToolByName(context, 'portal_catalog')
    lectures = catalog(object_provides=['isaw.events.interfaces.lecture.ILecture'])
    for lecture in lectures:
        new_lecture = copy_generic_fields(lecture)
        new_lecture.eventType = 'Lecture'
        remove_and_rename(lecture)

    performances = catalog(object_provides=['isaw.events.interfaces.performance.IPerformance'])
    for performance in performances:
        new_performance = copy_generic_fields(performance)
        new_performance.eventType = 'Performance'
        remove_and_rename(performance)

    exhibitions = catalog(object_provides=['isaw.events.interfaces.exhibition.IExhibition'])
    for exhibition in exhibitions:
        new_exhibition = copy_generic_fields(exhibition)
        new_exhibition.eventType = 'Exhibition'
        remove_and_rename(exhibition)

    sponsored_events = catalog(object_provides=['isaw.events.interfaces.sponsored.ISponsored'])
    for sponsored in sponsored_events:
        new_sponsored = copy_generic_fields(sponsored)
        new_sponsored.eventType = 'Sponsored'
        if new_sponsored.event_Sponsor_Name:
            if new_sponsored.event_Sponsor_Url:
                new_sponsored.text += '<p>Sponsored by: <a href="%s">%s</a></p>' % (new_sponsored.event_Sponsor_Url, new_sponsored.event_Sponsor_Name)
            else:
                new_sponsored.text += "<p>Sponsored by: %s</p>" % new_sponsored.event_Sponsor_Name
        remove_and_rename(sponsored)

    conferences = catalog(object_provides=['isaw.events.interfaces.conference.IConference'])
    for conference in conferences:
        new_conference = copy_generic_fields(conference)
        new_conference.eventType = 'Conference'
        remove_and_rename(conference)

    seminars = catalog(object_provides=['isaw.events.interfaces.seminar.ISeminar'])
    for seminar in seminars:
        new_seminar = copy_generic_fields(seminar)
        new_seminar.eventType = 'Seminar'
        remove_and_rename(seminar)

    general_events = catalog(object_provides=['isaw.events.interfaces.general.IGeneral'])
    for general in general_events:
        new_general = copy_generic_fields(general)
        new_general.eventType = 'General'
        remove_and_rename(general)

    properties.site_properties.enable_link_integrity_checks = old_check
