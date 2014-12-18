from Acquisition import aq_inner

from plone.app.layout.viewlets import ViewletBase
from collective.contentleadimage.config import IMAGE_FIELD_NAME


TYPE_DEFAULT = u'article'
TYPE_MAP = {
    u'profile': u'profile'
}


# Inspired by collective.opengraph
class OpenGraphTagViewlet(ViewletBase):
    """Viewlet which renders opengraph metadata for Facebook, etc."""

    def update(self):
        portal_state = self.context.restrictedTraverse(
            '@@plone_portal_state')
        context_state = self.context.restrictedTraverse(
            '@@plone_context_state')
        self.portal = portal_state.portal()

        self.metatags = []
        self.metatags.extend([(u'og:title', self.title),
                              (u'og:url', self.context.absolute_url()),
                              (u'og:image', self.image_url),
                              (u'og:site_name', self.sitename),
                              (u'og:description', self.description)])

        if context_state.is_portal_root():
            ctype = 'website'
            if getattr(self.view, '__name__', None) == u'search':
                self.metatags.append((u'og:type', u'article'))
                self.metatags.append((u'article:section', u'search'))
            else:
                self.metatags.append((u'og:type', u'website'))
        else:
            ctype = TYPE_MAP.get(self.context.portal_type, None)
            ctype = TYPE_DEFAULT if ctype is None else ctype
            if ctype:
                self.metatags.append((u'og:type', ctype))

        modified_date = self.context.ModificationDate()
        if ctype != 'website' and modified_date and modified_date != 'None':
            self.metatags.append((u'og:updated_time', modified_date))
            if ctype == u'article':
                self.metatags.append((u'article:modified_time',
                                      modified_date))

        if ctype == u'article':
            pub_date = self.context.EffectiveDate()
            if pub_date and pub_date != 'None':
                self.metatags.append((u'article:published_time', pub_date))

            expires_date = self.context.ExpirationDate()
            if expires_date and expires_date != 'None':
                self.metatags.append((u'article:expiration_time',
                                      expires_date))

            creator = self.context.Creator()
            if creator:
                self.metatags.append((u'article:author',
                                     creator.decode('utf8')))

            if self.context.portal_type == 'News Item':
                self.metatags.append((u'article:section', u'news'))
            elif self.context.portal_type == 'Event':
                self.metatags.append((u'article:section', u'event'))
            else:
                section = self.section
                if section:
                    self.metatags.append((u'article:section', section))

            for tag in self.context.Subject():
                if tag:
                    self.metatags.append((u'article:tag', tag.decode('utf8')))

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

        return u"%s/isaw_logo.png" % self.portal.absolute_url()

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
