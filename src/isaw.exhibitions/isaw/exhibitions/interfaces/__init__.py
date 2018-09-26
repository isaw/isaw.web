from collective import dexteritytextindexer
from plone.app.textfield import RichText
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
from isaw.exhibitions import exhibitionsMessageFactory as _


class IISAWExhibitionsLayer(Interface):
    """layer for package-specific component registrations."""


class IExhibitionObject(model.Schema):
    """Schema for Exhibition Objects."""

    full_title = schema.TextLine(title=_(u'Full Title'), required=False)
    title_detail = schema.TextLine(title=_(u'Title Detail'), required=False)
    artist = schema.TextLine(title=_(u'Artist'), required=False)
    author = schema.TextLine(title=_(u'Author'), required=False)
    copyist = schema.TextLine(title=_(u'Copyist'), required=False)
    download_link = schema.TextLine(title=_(u'Download Link'), required=False)
    download_link_text = schema.TextLine(title=_(u'Download Link Text'), required=False)
    download_link_type = schema.TextLine(title=_(u'Download Link Type'), required=False)
    translator = schema.TextLine(title=_(u'Translator'), required=False)
    copyright = schema.TextLine(title=_(u'Copyright Notice'), required=False)
    credits = schema.TextLine(title=_(u'Credit Line'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    dimensions = schema.TextLine(title=_(u'Dimensions'), required=False)
    exhibition_context = schema.TextLine(title=_(u'Context'), required=False)
    image = namedfile.NamedBlobImage(title=_(u'Lead Image'), required=False)
    alt = schema.TextLine(title=_(u'Alt Text'), required=False)
    inventory_num = schema.TextLine(title=_(u'Inventory Number'), required=True)
    lender = schema.TextLine(title=_(u'Lender'), required=False)
    lender_link = schema.URI(title=_(u'Lender Link'), required=False)
    medium = schema.TextLine(title=_(u'Medium'), required=False)
    not_after = schema.Int(title=_(u'Not After'), required=False)
    not_before = schema.Int(title=_(u'Not Before'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    object_language = schema.TextLine(title=_(u'Object Language'), required=False)
    object_location = schema.TextLine(title=_(u'Object Location'), required=False)

    dexteritytextindexer.searchable('text')
    text = RichText(title=_(u'Body'), required=False)
    label = RichText(title=_(u'Label'), required=False)

    @invariant
    def alt_text_invariant(data):
        if data.image and not data.alt:
            raise Invalid(_(u'Alt text is required for images'))
