from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

#facultycv requires the pisa module for pdf view
import ho.pisa as pisa

class ProfileView(BrowserView):
    pass

class PdfView(BrowserView):
    """ pdf view"""

    def __call__(self):
        response = self.request.response
        title = self.context.Title()
        ftitle = "/tmp/%s_CV.pdf" % (title)
        filename = ftitle

        attachment = 'attachment; filename=%s' % (ftitle)
        f = file(filename, "wb")
        pdf_template = ViewPageTemplateFile('pdf-view.pt')(self)

        response.setHeader('Content-Type', 'application/pdf')
        response.setHeader('Content-Disposition', attachment);
        pdf = pisa.CreatePDF(pdf_template.encode("UTF-8"), response)
        f.flush()
        f.close()

        if not pdf.err:
            return response
        else:
            # Something is wrong 
            # Fledge this out later
            pass
