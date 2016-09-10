# Disable the HomeFolderLocator from plone.app.iterate
from plone.app.iterate.containers import HomeFolderLocator
HomeFolderLocator.available = False


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
