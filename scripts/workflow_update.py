import sys
import argparse
import transaction

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest
from zope.component.hooks import setSite


def spoofRequest(app):
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    user = app.acl_users.getUser('admin')
    newSecurityManager(None, user.__of__(app.acl_users))
    return makerequest(app)


def getSite(app, args):
    site_name = args.site
    site = app.unrestrictedTraverse(site_name)
    site.setupCurrentSkin(app.REQUEST)
    setSite(site)
    return site


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update workflow default state.')
    parser.add_argument('--site',
                        help='Path to plone site from root. Defaults to "Plone"',
                        default='Plone')
    parser.add_argument('--path',
                        help='Path to add missing content state',
                        default='guide',)
    parser.add_argument('--to',
                        help='Workflow id to update',
                        default='isaw_intranet_workflow')
    parser.add_argument('--source',
                        help='Workflow from which to get current status',
                        default='one_state_workflow')
    parser.add_argument('--types',
                        help='Content types to update',
                        default='File',)
    if sys.argv[0].endswith('/interpreter'):
        del sys.argv[0]
        del sys.argv[1]
    args = parser.parse_args()
    count = 0
    app = spoofRequest(app)
    site = getSite(app, args)
    path = '/'.join(['', args.site, args.path])
    catalog = getToolByName(site, 'portal_catalog')
    wf_tool = getToolByName(site, 'portal_workflow')
    from_wf = args.source
    wf_id = args.to
    types = args.types.split(',')
    brains = catalog.unrestrictedSearchResults(
        portal_type=types,
        path={'query': path, 'depth': -1}
    )
    for b in brains:
        ob = b.getObject()
        status = wf_tool.getStatusOf(wf_id, ob)
        if status is not None and status != 'published':
            continue
        from_state = wf_tool.getStatusOf(from_wf, ob)
        if from_state:
            wf_tool.setStatusOf(wf_id, ob, from_state)
        count += 1

    print("Update default state for {} objects".format(count))
    transaction.commit()
