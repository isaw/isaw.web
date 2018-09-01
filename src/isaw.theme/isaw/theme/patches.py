from cgi import escape

from OFS.Image import Image
from Products.Archetypes.Field import ImageField
from Products.PluginIndexes.UUIDIndex.UUIDIndex import UUIDIndex


def allow_not_uuid():
    UUIDIndex.query_options = tuple(UUIDIndex.query_options) + ('not',)


def _wcag_tag(self, instance, scale=None, height=None, width=None, alt=None,
              css_class=None, title=None, **kwargs):
    """"Accept title as parameter, but do not use in img tag, per WCAG"""
    image = self.getScale(instance, scale=scale)
    if image:
        img_width, img_height = self.getSize(instance, scale=scale)
    else:
        img_height = 0
        img_width = 0

    if height is None:
        height = img_height
    if width is None:
        width = img_width

    url = instance.absolute_url()
    if scale:
        url += '/' + self.getScaleName(scale)
    else:
        url += '/' + self.getName()

    if not alt:
        alt = instance.Title()

    values = {'src': url,
              'alt': escape(alt, quote=True),
              'height': height,
              'width': width,
              }

    result = '<img src="%(src)s" alt="%(alt)s" '\
                'height="%(height)s" width="%(width)s"' % values

    if css_class is not None:
        result = '%s class="%s"' % (result, css_class)

    for key, value in kwargs.items():
        if value:
            result = '%s %s="%s"' % (result, key, value)

    return '%s />' % result


def img_tag_no_title():
    ImageField.tag = _wcag_tag


def _wcag_ofs_tag(self, height=None, width=None, alt=None,
        scale=0, xscale=0, yscale=0, css_class=None, title=None, **args):

    if height is None: height=self.height
    if width is None:  width=self.width

    xdelta = xscale or scale
    ydelta = yscale or scale

    if xdelta and width:
        width =  str(int(round(int(width) * xdelta)))
    if ydelta and height:
        height = str(int(round(int(height) * ydelta)))

    result='<img src="%s"' % (self.absolute_url())

    if alt is None:
        alt=getattr(self, 'alt', '')
    result = '%s alt="%s"' % (result, escape(alt, 1))

    if height:
        result = '%s height="%s"' % (result, height)

    if width:
        result = '%s width="%s"' % (result, width)

    if css_class is not None:
        result = '%s class="%s"' % (result, css_class)

    for key in args.keys():
        value = args.get(key)
        if value:
            result = '%s %s="%s"' % (result, key, value)

    return '%s />' % result


def ofs_img_tag_no_title():
    Image.tag = _wcag_ofs_tag
