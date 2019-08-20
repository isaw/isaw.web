import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from isaw.policy.testing import ISAW_POLICY_INTEGRATION_TESTING
from isaw.policy.config import SSO_PLUGIN_ID
from isaw.policy.setuphandlers import activate_and_prioritize_spsso_auth_plugin
from isaw.policy.setuphandlers import add_loggedin_page
from isaw.policy.setuphandlers import add_saml_authority_object
from isaw.policy.setuphandlers import add_spsso_plugin_and_its_children
from isaw.policy.setuphandlers import setup_saml2


class TestSAML2Setup(unittest.TestCase):
    layer = ISAW_POLICY_INTEGRATION_TESTING
    implemented_plugin_types = (
        "IAuthenticationPlugin",
        "IChallengePlugin",
        "ICredentialsResetPlugin",
        "IExtractionPlugin",
        "IPropertiesPlugin",
    )

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.acl_users = self.portal.acl_users
        self.workflow = self.portal.portal_workflow
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_saml_authority_added_at_site_root(self):
        add_saml_authority_object(self.portal)
        self.assertTrue('saml2auth' in self.portal)

    def test_saml_authority_has_identity_provider_entity_added(self):
        authority = add_saml_authority_object(self.portal)
        self.assertIn(
            'SSO Identity Provider',
            authority.list_entities()[0].title
        )

    def test_saml_authority_pem_and_der_certs_set(self):
        authority = add_saml_authority_object(self.portal)
        self.assertEqual(authority.certificate, '../../conf/isaw-staging.der')
        self.assertEqual(authority.private_key, '../../conf/isaw-staging.pem')

    def test_spsso_plugin_added_to_acl_users(self):
        add_spsso_plugin_and_its_children(self.portal)
        self.assertTrue(SSO_PLUGIN_ID in self.acl_users)

    def test_spsso_plugin_has_attribute_consuming_service(self):
        plugin = add_spsso_plugin_and_its_children(self.portal)
        self.assertTrue('saml2sp-attribute-service' in plugin)

    def test_spsso_plugin_requests_correct_attributes(self):
        plugin = add_spsso_plugin_and_its_children(self.portal)
        service = plugin._getOb('saml2sp-attribute-service')
        self.assertTrue('sn' in service)
        self.assertTrue('givenName' in service)
        self.assertTrue('eduPersonPrincipalName' in service)

    def test_add_loggedin_page_adds_private_page_visible_to_authenticated(self):
        add_loggedin_page(self.portal)
        self.assertIn('loggedin', self.portal.objectIds())
        page = self.portal['loggedin']
        self.assertEqual(
            'draft', self.workflow.getInfoFor(page, 'review_state', '')
        )
        local_roles = page.get_local_roles()
        self.assertIn(('Authenticated', ('Reader',)), local_roles)

    def test_activate_and_prioritize_spsso_auth_plugin_activates(self):
        add_spsso_plugin_and_its_children(self.portal)
        activate_and_prioritize_spsso_auth_plugin(self.portal)
        for iface in self.implemented_plugin_types:
            self.assertIn(
                SSO_PLUGIN_ID,
                self.acl_users.plugins.getAllPlugins(iface)['active']
            )

    def test_spsso_auth_plugin_prioritizes(self):
        add_spsso_plugin_and_its_children(self.portal)
        activate_and_prioritize_spsso_auth_plugin(self.portal)
        for iface in self.implemented_plugin_types:
            self.assertEqual(
                SSO_PLUGIN_ID, self.acl_users.plugins.getAllPlugins(iface)['active'][0]
            )

    def test_top_level_runner(self):
        self.assertTrue(setup_saml2(self.portal))

    def test_top_level_runner_idempotent(self):
        self.assertTrue(setup_saml2(self.portal))
        self.assertTrue(setup_saml2(self.portal))
