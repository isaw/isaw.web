from zope.app.file.image import Image as ImageBase
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl

class Image(ImageBase, DefaultDublinCoreImpl):
    """
    We need our own Image class here to mix in Dublin Core, since the
    zope image object uses zope 3 machinery to attribute dublin core
    properties which doesn't work here. Or at least I can't get one of
    these image objects to adapt to
    zope.dublincore.interfaces.IWriteZopeDublinCore
    """
    def __init__(self, data=''):
        ImageBase.__init__(self, data)
        DefaultDublinCoreImpl.__init__(self)
