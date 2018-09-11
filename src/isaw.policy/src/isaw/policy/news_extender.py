from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.public import AnnotationStorage
from Products.ATContentTypes.interfaces import IATNewsItem
from Products.ATContentTypes.content.newsitem import ATNewsItem
from isaw.policy.interfaces import IISAWPolicyLayer
from . import MessageFactory as _


IMAGE_ALT_FIELD_NAME = 'image_alt'


# alt text should be required when uploading lead images
def post_validate(self, REQUEST=None, errors=None):
    upload = REQUEST.get('image_file', None)
    delete = REQUEST.get('image_delete', None)
    alt = REQUEST.get(IMAGE_ALT_FIELD_NAME, None)
    errmsg = "Alt text is required when uploading an image"
    if upload and not alt:
        errors[IMAGE_ALT_FIELD_NAME] = errmsg
    if delete and delete != 'delete' and not alt:
        errors[IMAGE_ALT_FIELD_NAME] = errmsg
    if errors:
        return errors
ATNewsItem.post_validate = post_validate


class ImageAltTextField(ExtensionField, StringField):
    """Alt text for WCAG A compliance"""


altTextField = ImageAltTextField(
    IMAGE_ALT_FIELD_NAME,
    required=False,
    searchable=False,
    storage=AnnotationStorage(),
    widget=StringWidget(
        label=_(u"Lead image alt text"),
        description=_(u"Accessibility guidelines require an alt text"),
    ),
)


class NewsItemExtender(object):
    adapts(IATNewsItem)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = IISAWPolicyLayer

    fields = [
        altTextField,
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        """
        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.

        Move alt text field just after the image
        """
        default = original.get('default', None)
        if default:
            index = default.index('image')
            if IMAGE_ALT_FIELD_NAME in default:
                default.remove(IMAGE_ALT_FIELD_NAME)
                default.insert(index+1, IMAGE_ALT_FIELD_NAME)
        return original
