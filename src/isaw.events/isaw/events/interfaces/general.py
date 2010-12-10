from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from isaw.events import IsawEventMessageFactory as _

class IGeneral(Interface):
    """General Event"""
    
    # -*- schema definition goes here -*-
