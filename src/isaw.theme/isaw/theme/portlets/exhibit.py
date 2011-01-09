from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from isaw.theme.portlets.widget import ImageWidget

class IExhibitPortlet(IPortletDataProvider):

    image = schema.Field(
            title=_(u'Exhibit Image'),
            description=_(u'A small image from the featured exhibition'),
            required=False)

    exhibit_title = schema.TextLine(
            title=_(u'Title of Current Exhibit'),
            description=_(u'Title to appear on the front page about current exhibit.'),
            required=False)
            
    exhibit_description = schema.Text(
            title=_(u'Description of Current Exhibit'),
            description=_(u'Description of current exhibit as it will appear on the front page.'),
            required=False)

class Assignment(base.Assignment):
    implements(IExhibitPortlet)

    header = u''
    image = None
    assignment_context_path = None

    def __init__(self,
                 image=None, 
                 exhibit_title=None,
                 exhibit_description=None,
                 header=None,
                 assignment_context_path=None):

        self.image = image
        self.exhibit_title = exhibit_title
        self.exhibit_description = exhibit_description
        self.header = header
        self.assignment_context_path = assignment_context_path

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return _(u"Exhibit Portlet")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('exhibit.pt')

    def title(self):
        return self.data.exhibit_title

    def description(self):
        return self.data.exhibit_description

    def image(self):
        if self.data.image:
            state=getMultiAdapter((self.context, self.request),
                               name="plone_portal_state")
            portal=state.portal()
            assignment_url = \
                 portal.unrestrictedTraverse(
              self.data.assignment_context_path).absolute_url()
            width = self.data.image.width
            height = self.data.image.height
            return "<img src='%s/%s/@@image' width='%s' height='%s' alt='%s'/>" % \
                 (assignment_url,
                 self.data.__name__,
                 str(width),
                 str(height),
                 self.data.exhibit_description)
        return None

class AddForm(base.AddForm):
    form_fields = form.Fields(IExhibitPortlet)
    form_fields['image'].custom_widget = ImageWidget
    label = _(u"Add Exhibitions Portlet")
#    description = _(u"This portlet displays exhibition frontpage copy")

    def create(self, data):
        #assignment_context_path = \
        #            '/'.join(self.context.__parent__.getPhysicalPath())
        return Assignment(**data)

class EditForm(base.EditForm):
    
    form_fields = form.Fields(IExhibitPortlet)
    form_fields['image'].custom_widget = ImageWidget
    description = _(u"This portlet displays exhibition front page copy.")

