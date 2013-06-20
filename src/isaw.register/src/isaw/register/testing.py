from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class IsawregisterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import isaw.register
        xmlconfig.file(
            'configure.zcml',
            isaw.register,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'isaw.register:default')

ISAW_REGISTER_FIXTURE = IsawregisterLayer()
ISAW_REGISTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ISAW_REGISTER_FIXTURE,),
    name="IsawregisterLayer:Integration"
)
