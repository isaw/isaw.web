from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface import IATEvent
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.Archetypes import atapi

from isaw.policy.interfaces import IISAWPolicyLayer


class _ExtensionStringField(ExtensionField, atapi.StringField):
    pass


class _ExtensionBoolField(ExtensionField, atapi.BooleanField):
    pass


class ISAWEventExtender(object):
    adapts(IATEvent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender,
               ISchemaModifier)
    layer = IISAWPolicyLayer

    fields = [
        _ExtensionStringField(
            "subtitle",
            widget=atapi.StringWidget(
                description=u"",
                label=u"Subtitle"
            )
        ),
        _ExtensionStringField(
            "eventType",
            vocabulary=(("General", (u"General")),
                        ("Conference", (u"Conference")),
                        ("Exhibition", (u"Exhibition")),
                        ("Lecture", (u"Lecture")),
                        ("Performance", (u"Performance")),
                        ("Seminar", (u"Seminar")),
                        ("Sponsored", (u"Sponsored")),
                        ),
            enforceVocabulary=True,
            required=True,
            widget = atapi.SelectionWidget(
                label=u'Event Type',
                description='Select the most appropriate term to '
                            'describe the nature of this event.',
            ),
        ),
        _ExtensionStringField(
            "speaker",
            widget=atapi.StringWidget(
                description=u"If this event features a single speaker, "
                            u"enter their name in this field.",
                label=u"Speaker"
            )
        ),
        _ExtensionStringField(
            "speakerAffiliation",
            widget=atapi.StringWidget(
                description=u"If this event features a single speaker, enter "
                            u"their institutional affilication in this field.",
                label=u"Speaker Affiliation"
            )
        ),
        _ExtensionStringField(
            "rsvpRequired",
            widget = atapi.BooleanWidget(
                description=u"If an RSVP is required, check this box.",
                label=u"RSVP Required"
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.

        @param schematas: Dictonary of schemata name -> field lists

        @return: Dictionary of reordered field lists per schemata.
        """
        default_schema = schematas.get("default", [])
        for fname in ['subtitle', 'eventType', 'speaker',
                      'speakerAffiliation', 'rsvpRequired']:
            try:
                default_schema.remove(fname)
            except ValueError:
                pass

        desc_pos = default_schema.index('description') + 1
        default_schema.insert(desc_pos - 1, 'subtitle')
        default_schema[desc_pos + 1:desc_pos + 1] = ['eventType', 'speaker',
                                                     'speakerAffiliation']
        default_schema.append('rsvpRequired')
        return schematas

    def getFields(self):
        return self.fields
