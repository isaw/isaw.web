from Products.CMFCore.utils import getToolByName

def sync(context, event):
    """ Sync user data across multiple systems """

    c = dir(context)
    e = dir(event)

    print c
    print "\n"
    print e
    

    # Portal Membership - traverse
    mt = getToolByName(context, 'portal_membership')

    l = dir(context)
    print l

    print "Properties\n"
    

    # Bodyblank properties
    name = mt.getName()
    print name
    member = mt.getMemberById(name)
    fullname = member.getProperty("fullname")
    print fullname
    email = member.getProperty("email")
    print email
    user = member.getUser()
    print user
    other = member.getUserName()
    print other
    what = member.getUserId()
    print what
    login = member.getProperty("login")
    print login
    
