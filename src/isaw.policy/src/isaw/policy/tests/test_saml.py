import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from isaw.policy.testing import ISAW_POLICY_INTEGRATION_TESTING
from isaw.policy.setuphandlers import add_saml_authority_object
from isaw.policy.setuphandlers import add_spsso_plugin


class TestSAML2Setup(unittest.TestCase):

    layer = ISAW_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_saml_authority_added_at_site_root(self):
        add_saml_authority_object(self.portal)
        self.assertTrue('saml2auth' in self.portal)

    def test_spsso_plugin_added_to_acl_users(self):
        add_spsso_plugin(self.portal)
        self.assertTrue('saml2sp' in self.portal.acl_users)

    def test_spsso_plugin_has_attribute_consuming_service(self):
        plugin = add_spsso_plugin(self.portal)
        self.assertTrue('saml2sp-attribute-service' in plugin)
