from zope.component import adapts
from plone.app.blob.interfaces import IATBlobImage
from plone.cachepurging.paths import TraversablePurgePaths
from Products.CMFCore.utils import getToolByName
from collective.contentleadimage.config import (IMAGE_FIELD_NAME,
                                                IMAGE_SCALE_NAME,
                                                IMAGE_SIZES
                                                )
from collective.contentleadimage.interfaces import ILeadImageable


class ImagePurgePaths(TraversablePurgePaths):
    """Cache purger for content image content"""
    adapts(IATBlobImage)
    image_names = ('image',)

    def _image_scales(self):
        props = getToolByName(self.context,
                              'portal_properties').imaging_properties
        return [p.split()[0] for p in props.getProperty('allowed_sizes', [])]

    def getRelativePaths(self):
        paths = []
        base = '/' + self.context.virtual_url_path().rstrip('/')
        for name in self.image_names:
            paths.append('{}/{}'.format(base, name))
            paths.append('{}/@@images/{}'.format(base, name))
            for scale in self._image_scales():
                paths.append('{}/@@images/{}/{}'.format(base, name, scale))
                paths.append('{}/{}_{}'.format(base, name, scale))
        return paths


class LeadimagePurgePaths(ImagePurgePaths):
    adapts(ILeadImageable)
    image_names = (IMAGE_FIELD_NAME,)

    def _image_scales(self):
        scales = set(super(LeadimagePurgePaths, self)._image_scales())
        scales.add(IMAGE_SCALE_NAME)
        scales |= set(IMAGE_SIZES.keys())
        return list(scales)
