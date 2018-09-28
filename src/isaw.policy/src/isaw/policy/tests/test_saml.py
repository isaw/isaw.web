import unittest2 as unittest
from isaw.policy.testing import ISAW_POLICY_INTEGRATION_TESTING
from isaw.policy.setuphandlers import add_saml_authority_object
from isaw.policy.setuphandlers import add_spsso_plugin_and_its_children
from isaw.policy.setuphandlers import setup_saml2


class TestSAML2Setup(unittest.TestCase):

    layer = ISAW_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_saml_authority_added_at_site_root(self):
        add_saml_authority_object(self.portal)
        self.assertTrue('saml2auth' in self.portal)

    def test_saml_authority_pem_and_der_certs_set(self):
        authority = add_saml_authority_object(self.portal)
        import pdb; pdb.set_trace()
        self.assertEqual(authority.certificate, '../../conf/isaw-staging.der')
        self.assertEqual(authority.private_key, '../../conf/isaw-staging.pem')

    def test_spsso_plugin_added_to_acl_users(self):
        add_spsso_plugin_and_its_children(self.portal)
        self.assertTrue('saml2sp' in self.portal.acl_users)

    def test_spsso_plugin_has_attribute_consuming_service(self):
        plugin = add_spsso_plugin_and_its_children(self.portal)
        self.assertTrue('saml2sp-attribute-service' in plugin)

    def test_spsso_plugin_requests_correct_attributes(self):
        plugin = add_spsso_plugin_and_its_children(self.portal)
        service = plugin._getOb('saml2sp-attribute-service')
        self.assertTrue('sn' in service)
        self.assertTrue('givenName' in service)
        self.assertTrue('eduPersonPrincipalName' in service)

    def test_top_level_runner(self):
        self.assertTrue(setup_saml2(self.portal))
