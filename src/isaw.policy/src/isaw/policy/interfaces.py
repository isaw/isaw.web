from zope.interface import Interface
from zope.schema import List, TextLine, Text, Tuple, URI
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from isaw.bibitems.interfaces import IBibliographicItem
from isaw.policy import MessageFactory as _
from plone.app.textfield import RichText
from plone.dexterity.browser import add
from plone.directives import form
from z3c.form import widget


class IISAWPolicyLayer(Interface):
    """Marker layer interface for ISAW Site"""


class ILOCSubject(form.Schema):
    uri = URI(title=_(u'LOC URI'))
    text = TextLine(title=_(u'Subject'))


class IISAWPublication(form.Schema):
    short_title = TextLine(title=_(u'Short Title'))
    form.order_after(short_title='IBibliographicItem.title')

    tag_line = TextLine(title=_(u'Tag Line'),
                        required=False)
    form.order_after(tag_line='IBibliographicItem.description')

    authors = Tuple(
        title=_(u'Authors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )
    form.order_before(authors='IBibliographicItem.citation_detail')

    editors = Tuple(
        title=_(u'Editors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )
    form.order_before(editors='IBibliographicItem.citation_detail')

    contributors = Tuple(
        title=_(u'Contributors'),
        description=_(u'Enter username or plain-text name, one per line'),
        value_type=TextLine(),
        required=False,
        missing_value=(),
    )
    form.order_before(contributors='IBibliographicItem.citation_detail')

    publisher = TextLine(title=_(u'Publisher'),
                         required=False)
    form.order_after(publisher='IBibliographicItem.alternate_uri')

    publisher_uri = URI(title=_(u'Publisher URI'),
                        required=False)
    form.order_after(publisher_uri='publisher')

    review_uri = URI(title=_(u'Review URI'),
                     required=False)
    form.order_after(review_uri='publisher_uri')

    isbn = TextLine(title=_(u'ISBN'),
                    required=False)
    form.order_after(isbn='review_uri')

    issn = TextLine(title=_(u'ISSN'),
                    required=False)
    form.order_after(issn='isbn')

    doi = TextLine(title=_(u'DOI'),
                   required=False)
    form.order_after(doi='issn')

    text = RichText(
        title=_(u'Body'),
        default_mime_type='text/html',
        allowed_mime_types=('text/html',),
        output_mime_type='text/x-safe-html',
        required=False,
    )
    form.order_after(text='doi')

    loc_subjects = List(title=_(u'LOC Subjects'),
                        value_type=DictRow(title=u'Subject',
                                           schema=ILOCSubject),
                        required=False)
    form.widget(loc_subjects=DataGridFieldFactory)
    form.order_after(loc_subjects='*')


class PublicationAddForm(add.DefaultAddForm):
    portal_type = 'isaw.policy.publication'


class PublicationAddView(add.DefaultAddView):
    form = PublicationAddForm


PubBibURILabel = widget.StaticWidgetAttribute(
    u'Alternate Bibliographic URI',
    context=IISAWPublication, field=IBibliographicItem['bibliographic_uri']
)

PubAddBibURILabel = widget.StaticWidgetAttribute(
    u'Alternate Bibliographic URI',
    view=PublicationAddForm, field=IBibliographicItem['bibliographic_uri']
)

PubTitleLabel = widget.StaticWidgetAttribute(
    u'Full Title',
    context=IISAWPublication, field=IBibliographicItem['title']
)

PubAddTitleLabel = widget.StaticWidgetAttribute(
    u'Full Title',
    view=PublicationAddForm, field=IBibliographicItem['title']
)
