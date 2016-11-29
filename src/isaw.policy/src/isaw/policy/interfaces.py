from zope.interface import Interface
from zope.schema import List, Text, TextLine, Tuple, URI
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from isaw.bibitems.interfaces import IBibliographicItem
from isaw.policy import MessageFactory as _
from plone.app.textfield import RichText
from plone.dexterity.browser import add
from plone.directives import form
from plone.namedfile import field as namedfile
from z3c.form import widget
from z3c.form.browser.textlines import TextLinesFieldWidget


class IISAWPolicyLayer(Interface):
    """Marker layer interface for ISAW Site"""


class IISAWPublication(form.Schema):
    title = TextLine(
        title=_(u"Title"),
        description=_(u"The short title of the bibliographic reference."),
    )

    short_title = TextLine(title=_(u'Short Title'))

    description = Text(
        title=_(u'Summary'),
        description=_(u'Used in item listings and search results.'),
        required=False,
        missing_value=u'',
    )

    tag_line = TextLine(title=_(u'Tag Line'), required=False)

    authors = Tuple(
        title=_(u'Authors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )

    editors = Tuple(
        title=_(u'Editors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )

    contributors = Tuple(
        title=_(u'Contributors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )

    parent_title = TextLine(title=_(u'Parent Title'), required=False)

    parent_uri = URI(title=_(u'Parent URI'), required=False)

    volume = TextLine(title=_(u'Volume'), required=False)

    date_of_publication = TextLine(
        title=_(u'Publication Date'),
        description=_(u'Enter the date on which this publication was issued'),
        required=False)

    range = TextLine(
        title=_(u"Range"),
        required=False,
    )

    formatted_citation = TextLine(
        title=_(u"Formatted Citation"),
        required=False,
    )

    bibliographic_uri = URI(
        title=_(u"Zotero URI"),
        description=_(u"This is a URI to a Zotero bibliographic reference."),
        required=False,
    )

    worldcat_uri = URI(
        title=_(u"Worldcat URI"),
        description=_(u"This is a URI to access the identified resource."),
        required=False,
    )

    publisher = TextLine(title=_(u'Publisher'),
                         required=False)

    publisher_uri = URI(title=_(u'Publisher URI'),
                        required=False)

    extent = TextLine(title=_(u'Extent'),
                         required=False)

    access_uris = List(title=_(u'Access URIs (one per line)'),
                        value_type=URI(title=u'URI'),
                        required=False)
    form.widget('access_uris', TextLinesFieldWidget)

    review_uris = List(title=_(u'Review URIs (one per line)'),
                        value_type=URI(title=u'URI'),
                        required=False)
    form.widget('review_uris', TextLinesFieldWidget)

    order_uris = List(title=_(u'Order URIs (one per line)'),
                        value_type=URI(title=u'URI'),
                        required=False)
    form.widget('order_uris', TextLinesFieldWidget)


    image = namedfile.NamedBlobImage(
        title=_(u'label_leadimage', default=u'Lead Image'),
        description=_(u'help_leadimage', default=u''),
        required=False,
    )

    image_caption = TextLine(
        title=_(u'label_leadimage_caption', default=u'Lead Image Caption'),
        description=_(u'help_leadimage_caption', default=u''),
        required=False,
    )

    isbn = TextLine(title=_(u'ISBN'),
                    required=False)

    issn = TextLine(title=_(u'ISSN'),
                    required=False)

    doi = TextLine(title=_(u'DOI'),
                   required=False)

    text = RichText(
        title=_(u'Body'),
        default_mime_type='text/html',
        allowed_mime_types=('text/html',),
        output_mime_type='text/x-safe-html',
        required=False,
    )


class PublicationAddForm(add.DefaultAddForm):
    portal_type = 'isaw.policy.publication'


class PublicationAddView(add.DefaultAddView):
    form = PublicationAddForm


PubTitleLabel = widget.StaticWidgetAttribute(
    u'Full Title',
    context=IISAWPublication, field=IBibliographicItem['title']
)

PubAddTitleLabel = widget.StaticWidgetAttribute(
    u'Full Title',
    view=PublicationAddForm, field=IBibliographicItem['title']
)
