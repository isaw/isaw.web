from zope import schema
from zope.interface import Interface

from zope.container.constraints import contains
from zope.container.constraints import containers

from isaw.events import IsawEventMessageFactory as _

class ILecture(Interface):
    """Lecture Event"""

    # -*- schema definition goes here -*-
