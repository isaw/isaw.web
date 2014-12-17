from Acquisition import aq_inner

from plone.app.layout.viewlets import ViewletBase
from collective.contentleadimage.config import IMAGE_FIELD_NAME


TYPE_DEFAULT = 'article'
TYPE_MAP = {
    'Folder': '',
}


# Inspired by collective.opengraph
class OpenGraphTagViewlet(ViewletBase):
    """Viewlet which renders opengraph metadata for Facebook, etc."""

    def update(self):
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        self.portal = portal_state.portal()

        self.metatags = []
        self.metatags.extend([('og:title', self.title),
                              ('og:url', self.context.absolute_url()),
                              ('og:image', self.image_url),
                              ('og:site_name', self.sitename),
                              ('og:description', self.description)])

        ctype = TYPE_MAP.get(self.context.portal_type, None)
        ctype = TYPE_DEFAULT if ctype is None else ctype
        if ctype:
            self.metatags.append(('og:type', ctype))

        if ctype == 'article':
            pub_date = self.context.EffectiveDate()
            if pub_date and pub_date != 'None':
                self.metatags.append(('article:published_time', pub_date))

            modified_date = self.context.ModificationDate()
            if modified_date and modified_date != 'None':
                self.metatags.append(('article:modified_time', modified_date))

            expires_date = self.context.ExpirationDate()
            if expires_date and expires_date != 'None':
                self.metatags.append(('article:expiration_time', expires_date))

            creator = self.context.Creator()
            if creator:
                self.metatags.append(('article:author',
                                     creator.decode('utf8')))

            section = self.section
            if section:
                self.metatags.append(('article:section', section))

            for tag in self.context.Subject():
                self.metatags.append(('article.tag', tag.decode('utf8')))

    @property
    def image_url(self):
        """Return an image url for the context in that order
        - context image field
        - context lead image field
        - portal logo
        """
        context = aq_inner(self.context)
        obj_url = context.absolute_url()
        if hasattr(context, 'getField'):
            field = self.context.getField('image')
            if not field:
                field = context.getField(IMAGE_FIELD_NAME)

            if field and field.get_size(context) > 0:
                return u'%s/%s_%s' % (obj_url, field.getName(), 'thumb')

        return u"%s/logo.jpg" % self.portal.absolute_url()

    @property
    def description(self):
        return self.context.Description().decode('utf8')

    @property
    def title(self):
        return self.context.Title().decode('utf8')

    @property
    def sitename(self):
        return self.portal.Title().decode('utf8')

    @property
    def section(self):
        path = self.context.getPhysicalPath()
        portal_path = self.portal.getPhysicalPath()
        if len(path) > (len(portal_path) + 1):
            section = self.portal.unrestrictedTraverse(path[len(portal_path)])
            return section.Title().decode('utf-8')
