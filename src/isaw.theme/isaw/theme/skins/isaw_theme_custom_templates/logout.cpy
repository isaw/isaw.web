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

request = context.REQUEST

mt = getToolByName(context, 'portal_membership')
mt.logoutUser(request)

from Products.CMFPlone.utils import transaction_note
transaction_note('Logged out')

# After logging out of Plone, redirect to the NYU logout page:
nyu_logout_url = 'https://home.nyu.edu/logout'
request.response.redirect(nyu_logout_url)
return
