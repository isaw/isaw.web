# This needs a lot of work and unit testing for failures
# As failure occurs, and it will, especially with the printer routine below
# a test should be added - christopher.warner@nyu.edu

from zope.interface import Interface
from zope import schema
from zope.component import getUtility
from Products.Five.browser import BrowserView

import xmlrpclib
import time
from randomdotorg import RandomDotOrg

from zope.formlib import form
from five.formlib import formbase

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from zope.event import notify
from collective.progressbar.events import InitialiseProgressBar
from collective.progressbar.events import ProgressBar
from collective.progressbar.events import UpdateProgressEvent
from collective.progressbar.events import ProgressState

from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from plone import api
from selenium import webdriver
from pyvirtualdisplay import Display

import smtplib
from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused 

import signal, os

# yeah i know, i know - christopher.warner@nyu.edu
issue_tracker = xmlrpclib.ServerProxy('http://admin:M4d!s0n@automaton.isaw.nyu.edu:8082/help/', allow_none=True)

random = RandomDotOrg()

def SIGCHLDReaper(signum, frame):
    print "%s %s" % (signum, frame)
    os.waitpid(-1, os.WNOHANG)

signal.signal(signal.SIGCHLD, SIGCHLDReaper)

def checkEmailAddress(value):
    portal = getUtility(ISiteRoot)
    reg_tool = getToolByName(portal, 'portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True

class ISiteWideUserForm(Interface):

    fullname = schema.TextLine(title=u"Fullname",
                            description=u"Enter full name, e.g. John Smith.",
                            required=True)

    email = schema.ASCIILine(title=u"Email",
                            description=u"Enter an email address. This resembles netid@nyu.edu",
                            required=True,
                            constraint=checkEmailAddress)

class SiteWideUserForm(formbase.PageForm):
    form_fields = form.FormFields(ISiteWideUserForm)

    label = (u"Add a new sitewide user (website, copiers, ticket system)")
    description = (u"Onboard a new sitewide user to all ISAW systems")
    

    @form.action(u"Add new user")
    def action_send(self, action, data):
        """ Add's new user and then an email is sent """
        context = aq_inner(self.context)
        urltool = getToolByName(context, 'portal_url')
        siteroot = getUtility(ISiteRoot)
        portal = urltool.getPortalObject()

        userid = data['fullname']
        uemail = data['email']
        netid = uemail.partition("@")
        netid = netid[0]
        ucode = random.randint(10000, 99999)

        """ The ucode paradigm hopefully fades away in the future and is sync'd via SSO """

        #title = 'Adding sitewide user'
        #bar = ProgressBar(self.context, self.request, title, 'Working...')
        #notify(InitialiseProgressBar(bar))

        ###################
        # Plone user create

        plone_props = dict (
            fullname = userid,
        )

        user = api.user.create(
            username = uemail,
            email = uemail,
            properties=plone_props
        )

        #progress = ProgressState(self.request, 25)
        #notify(UpdateProgressEvent(progress))
        # Random five digit int for ucode

        ######################
        # Issue Tracker Create
        issue_tracker.create('user', "username=%s" % uemail, 
                                    "address=%s" % uemail, 
                                    "realname=%s" % userid, 
                                    "password=%s" % ucode,
                                    "organisation=nyu.edu",
                                    "roles=User" )
        #progress = ProgressState(self.request, 50)
        #notify(UpdateProgressEvent(progress))
             
        # Shorten it up 
        fullname = userid
        fullname.lower()
        fullname = fullname.split(' ')
        first = fullname[0][0:1]
        last = fullname[-1]
        shortname = first + last

        # Have to ignore SIGCHLD i'm not sure if it's virtualdisplay or selenium 
        display = Display(visible=0, size=(1024, 768)).start()
        display.start()

        ######################
        # Copiers user ceate
        ### LANIER345.ISAW.NYU.EDU
        baseURL = 'http://admin:''@lanier345.isaw.nyu.edu/web/entry/en/address/adrsList.cgi'
        ffdriver = webdriver.Firefox()
        time.sleep(2)
        ffdriver.get(baseURL)
        try:
            ffdriver.find_element_by_xpath("//td[2]/div/a/nobr").click()
            ffdriver.find_element_by_name("entryNameIn").clear()
            ffdriver.find_element_by_name("entryNameIn").send_keys(userid)
            ffdriver.find_element_by_name("entryDisplayNameIn").clear()
            ffdriver.find_element_by_name("entryDisplayNameIn").send_keys(shortname)
            ffdriver.find_element_by_name("userCodeIn").clear()
            ffdriver.find_element_by_name("userCodeIn").send_keys(ucode)
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[35]/td[4]/input[2]").click()
            ffdriver.find_element_by_name("availableFuncIn").click()

            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[1]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[2]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[3]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[30]/td[2]/input").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[30]/td[2]/input[2]").click()
            ffdriver.find_element_by_name("mailAddressIn").clear()
            ffdriver.find_element_by_name("mailAddressIn").send_keys(uemail)
            ffdriver.find_element_by_name("img_OK").click()
  
            time.sleep(3) 
            ### LANIER275.ISAW.NYU.EDU
            # Lets just make sure we have absolutely no problems with cookies and the
            # printers
            baseURL = 'http://laniercopier275.isaw.nyu.edu/web/guest/en/websys/webArch/authForm.cgi'
            ffdriver.get(baseURL)

            ### The cookiechecker from the lanier firmware will search for the session cookie
            ### Once it doesn't find it, it will throw an error message on
            ### subsequent call to the same baseURL we get the cookies and can proceed
            ffdriver.get(baseURL)
            ffdriver.find_element_by_name("userid_work").clear()
            ffdriver.find_element_by_name("userid_work").send_keys("admin")
            ffdriver.find_element_by_css_selector("input[type=\"submit\"]").click()
            
            ### We must slow down because we can't call clickAndWait()
            ### So we enter a race where the frame isn't available yet
            ### and generate a NoSuchFrameException. Should wrap and try/catch here

            ffdriver.switch_to_frame("work")
            ffdriver.find_element_by_id("ADRS_MENU").click()
            ffdriver.find_element_by_xpath("//table[2]/tbody/tr/td[3]/div/a/nobr").click()
            ffdriver.find_element_by_name("entryNameIn").clear()
            ffdriver.find_element_by_name("entryNameIn").send_keys(userid)
            ffdriver.find_element_by_name("entryDisplayNameIn").clear()
            ffdriver.find_element_by_name("entryDisplayNameIn").send_keys(shortname)
            ffdriver.find_element_by_name("userCodeIn").clear()
            ffdriver.find_element_by_name("userCodeIn").send_keys(ucode)
            ffdriver.find_element_by_name("availableFuncIn").click()

            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[1]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[2]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[29]/td[4]/input[3]").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[30]/td[2]/input").click()
            ffdriver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table/tbody/tr[30]/td[2]/input[2]").click()
            ffdriver.find_element_by_name("mailAddressIn").clear()
            ffdriver.find_element_by_name("mailAddressIn").send_keys(uemail)
            ffdriver.find_element_by_xpath("(//td[@onclick='javascript:Apply(); return false;'])[2]").click()

            ffdriver.quit()
        finally:
            display.stop() 

        #progress = ProgressState(self.request, 100)
        #notify(UpdateProgressEvent(progress))
 
        ucode = ucode + 50 
        
        email_charset = getattr(self, 'email_charset', 'UTF-8')
 
        email = portal.sitewide_user_email
        mail_text = email(charset=email_charset, request=context.REQUEST,
                            emailto=uemail, fullname=userid, usercode=ucode,
                            netid=netid)
        try:
            maildaemon = getToolByName(self, 'MailHost')
            return maildaemon.send(mail_text, mto=uemail,
                                    mfrom="isaw.it-group@nyu.edu",
                                    subject="ISAW User Code and Help Information",
                                    encode='text/plain',
                                    immediate=True)

        except SMTPRecipientsRefused:
            raise SMTPRecipientsRefused('Recipient address rejected')
 
        self.request.response.redirect(portal.absolute_url() + '/@@sitewide_user')
        IStatusMessage(self.request).addStatusMessage(_(u"Sitewide user " + userid + " added."), type=u'info')

        return

class SiteWideUser(BrowserView):
    pass
