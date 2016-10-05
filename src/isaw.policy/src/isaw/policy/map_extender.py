from Acquisition import aq_base
from zope.interface import Interface, implements, alsoProvides
from zope.component import adapts
from zope import schema

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from plone.formwidget.geolocation.field import GeolocationField
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm

from Products.Archetypes import atapi
from Products.Maps.field import LocationField, LocationWidget
from Products.Maps.content.Location import LocationMarker as BaseMarker
from Products.Maps.interfaces import IRichMarker


class IGeolocatable(Interface):
    """ Marker interface for content that should get the extra
    geolocation schemata.
    """


class ExtendedLocationField(ExtensionField, LocationField):
    pass


class ExtendedStringField(ExtensionField, atapi.StringField):
    pass


class MapSchemaExtender(object):
    implements(ISchemaExtender)

    _fields = [
        ExtendedLocationField(
            'geolocation',
            languageIndependent=1,
            required=False,
            default=(0, 0),
            validators=('isGeoLocation',),
            widget=LocationWidget(
                label='Geolocation',
                description="Enter a latitude and longitude in signed decimal degrees. Geodetic model is assumed to be WGS-1984."),
            schemata='Geolocation',
        ),
        ExtendedStringField(
            'pleiadesUrl',
            languageIndependent=1,
            required=False,
            validators=('isURL',),
            widget=atapi.StringWidget(
                label='Fetch coordinates from Pleiades ',
                description="Enter a pleiades place url to use to lookup place location data"),
            schemata='Geolocation',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields


class IGeolocationBehavior(model.Schema):
    """Form field for geolocation behavior"""
    geolocation = GeolocationField(
        title=u"Geolocation",
        description=u"Enter a latitude and longitude in signed decimal degrees. Geodetic model is assumed to be WGS-1984.",
        required=False)
    pleiades_url = schema.URI(title=u"Fetch coordinates from Pleiades URL",
                              required=False)
    directives.omitted('geolocation')
    directives.no_omit(IEditForm, 'geolocation')
    directives.no_omit(IAddForm, 'geolocation')
    fieldset('geolocation', label=u'Geolocation',
             fields=['geolocation', 'pleiades_url'])
alsoProvides(IGeolocationBehavior, IFormFieldProvider)


class ILocation(model.Schema):
    geolocation = GeolocationField(
        title=u"Geolocation",
        description=u"Longitude and latitude",
        required=False)


class LocationMarker(BaseMarker):
    implements(IRichMarker)
    adapts(IGeolocatable)

    @property
    def latitude(self):
        if getattr(aq_base(self.context), 'getField', None) is not None:
            location = self.context.getField('geolocation').getEditAccessor(self.context)()
            if not location or tuple(location) == (0, 0):
                return None
            return location[0]
        else:
            location = getattr(self.context, 'geolocation', None)
            if location is not None:
                return location.latitude

    @property
    def longitude(self):
        if getattr(aq_base(self.context), 'getField', None) is not None:
            location = self.context.getField('geolocation').getEditAccessor(self.context)()
            if not location or tuple(location) == (0, 0):
                return None
            return location[1]
        else:
            location = getattr(self.context, 'geolocation', None)
            if location is not None:
                return location.longitude

    @property
    def image_tag(self):
        try:
            if self.context.getImage():
                return self.context.tag(scale='thumb', css_class='map-image')
        except AttributeError:
            if getattr(aq_base(self.context), 'image', None):
                return self.context.image.tag(
                    scale='thumb',
                    css_class='map-image').encode('utf-8')
            return ''

    @property
    def icon(self):
        return 'Red Marker'

    @property
    def related_items(self):
        related = self.context.computeRelatedItems()
        result = []
        for obj in related:
            result.append({'title': obj.Title(),
                           'url': obj.absolute_url(),
                           'description': obj.Description()})
        return tuple(result)

    @property
    def contents(self):
        text = ''
        if self.context.getField('text'):
            text = self.context.getText()
        elif getattr(aq_base(self.context), 'text', None):
            text = self.context.text.output.encode('utf-8')
        if self.image_tag:
            text = self.image_tag + '\n' + text
        if text:
            return ({'title': "Info",
                     'text': text},)

    @property
    def layers(self):
        return []
