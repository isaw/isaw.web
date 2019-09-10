# Disable the HomeFolderLocator from plone.app.iterate
import logging
from zope.i18nmessageid import MessageFactory
from plone.app.iterate.containers import HomeFolderLocator
from . import patches
HomeFolderLocator.available = False


# Set up the i18n message factory for our package
MessageFactory = MessageFactory('isaw.policy')

logger = logging.getLogger('isaw.policy')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    patches.patch_saml_login()
