from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
import zope.schema as schema
from zope.interface import implements

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IFacultyCVUserDataSchema

class IFacultyCVUserDataSchema(IUserDataSchema):
    CVReference = schema.URI(
        title = u'CV Profile',
        description = u'Links to the URL of the faculty or staff member profile if it exists',
        required=False)
