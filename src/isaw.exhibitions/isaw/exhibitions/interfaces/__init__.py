from collective import dexteritytextindexer
from plone.app.textfield import RichText
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from isaw.exhibitions import exhibitionsMessageFactory as _


class IISAWExhibitionsLayer(Interface):
    """layer for package-specific component registrations."""


class IExhibitionObject(model.Schema):
    """Schema for Exhibition Objects."""

    artist = schema.TextLine(title=_(u'Artist'),
                             required=False)

    exhibition_context = schema.TextLine(title=_(u'Context'),
                                         required=False)

    date = schema.TextLine(title=_(u'Date'),
                           required=False)

    not_before = schema.Int(title=_(u'Not Before'),
                            required=False)

    not_after = schema.Int(title=_(u'Not After'),
                           required=False)

    dimensions = schema.TextLine(title=_(u'Dimensions'),
                                 required=False)

    inventory_num = schema.TextLine(title=_(u'Inventory Number'),
                                    required=True)

    lender = schema.TextLine(title=_(u'Lender'),
                             required=False)

    lender_link = schema.URI(title=_(u'Lender Link'),
                             required=False)

    medium = schema.TextLine(title=_(u'Medium'),
                             required=False)

    notes = schema.TextLine(title=_(u'Notes'),
                            required=False)

    credits = schema.TextLine(title=_(u'Credit Line'),
                              required=False)

    copyright = schema.TextLine(title=_(u'Copyright Notice'),
                                required=False)

    image = namedfile.NamedBlobImage(title=_(u'Lead Image'),
                                     required=False)

    dexteritytextindexer.searchable('text')
    text = RichText(title=_(u'Body'),
                    required=False)

    label = RichText(title=_(u'Label'),
                     required=False)
