## Controller Python Script "logout"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##title=Logout handler
##parameters=

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note

request = context.REQUEST

mt = getToolByName(context, 'portal_membership')
ssoView = context.restrictedTraverse('@@sso_view')

mt.logoutUser(request)
# After logging out of Plone, redirect to the NYU logout page.
ssoView.logout()

transaction_note('Logged out')
return
