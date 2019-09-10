# Disable the HomeFolderLocator from plone.app.iterate
import logging
from zope.i18nmessageid import MessageFactory

# XXX: Why did we disable home folder finding?
# from plone.app.iterate.containers import HomeFolderLocator
# HomeFolderLocator.available = False


# Set up the i18n message factory for our package
MessageFactory = MessageFactory('isaw.policy')

logger = logging.getLogger('isaw.policy')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
