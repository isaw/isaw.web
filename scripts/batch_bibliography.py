import argparse
import transaction
from urlparse import urlparse
from zope.component import queryUtility

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Testing.makerequest import makerequest
from zope.component.hooks import setSite

from isaw.bibitems.interfaces import IBibliographicURLIFetcher
from plone.dexterity.utils import createContentInContainer
from plone.namedfile.file import NamedBlobImage


def spoofRequest(app):
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    user = app.acl_users.getUser('admin')
    newSecurityManager(None, user.__of__(app.acl_users))
    return makerequest(app)


def getSite(app, args=None):
    if args:
        site_name = args.site
    else:
        site_name = 'Plone'
    site = app.unrestrictedTraverse(site_name)
    site.setupCurrentSkin(app.REQUEST)
    setSite(site)
    return site


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Bibliographic Items')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        dest='dry_run', help='No changes will be made.')
    parser.add_argument('--site',
                        help='Path to plone site from root. Defaults to "Plone"',
                        default='Plone')
    parser.add_argument('file', type=file, help='Path to import file')
    parser.add_argument('folder', help='Plone folder in which to create '
                                       'bibliographic items (will be created '
                                       'if not already present)')
    parser.add_argument('--title',
                        help='Title of new bibliographic folder (defaults to '
                        'captialized folder id)',
                        default='')

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    bib_file = args.file

    app = spoofRequest(app)
    site = getSite(app, args)

    print
    print "Starting batch content creation..."
    print

    parent = site
    folder = None
    path_parts = args.folder.split('/')
    for i, path in enumerate(path_parts):
        try:
            folder = parent.restrictedTraverse(path)
        except (KeyError, AttributeError):
            folder = None

        if folder is None:
            title = (args.title if i == (len(path_parts) - 1) else
                     path.title().replace('-', ' '))
            folder_id = parent.invokeFactory('Folder', id=path, title=title)
            parent = folder = parent[folder_id]
            print "Created new folder {}".format(folder.absolute_url(1))

    transforms = getToolByName(site, 'portal_transforms')
    for bib_url in bib_file.readlines():
        bib_url = bib_url.strip()
        hostname = urlparse(bib_url).hostname
        fetcher = queryUtility(IBibliographicURLIFetcher, name=hostname)
        data = fetcher.fetch(bib_url)
        if data.get('error'):
            print "Error fetching {}: {}".format(bib_url, data['error'])
            continue
        title = data.get(u'short_title') or data.get(u'title')
        bib_id = normalizeString(title) if title else bib_url.split('/')[-1]
        print "Creating Bibliographic Item: {}".format(bib_id)

        fields = {
            'title': title,
            'citation_detail': data.get(u'citation_detail'),
            'formatted_citation': data.get(u'formatted_citation'),
            'access_uri': data.get(u'access_uri'),
            'bibliographic_uri': bib_url,
        }
        if fields['formatted_citation']:
            fields['description'] = transforms.convertTo(
                'text/plain', data['formatted_citation'],
                mimetype='text/html'
            ).getData().strip()

        item = createContentInContainer(folder,
                                        'isaw.bibitems.bibitem',
                                        **fields)
        print 'Created Bibliographic Item with id "{}"'.format(item.id)
        print

    if args.dry_run:
        print "Dry run. No changes made in Plone."
    else:
        print "Updated content in Plone."
        transaction.commit()
