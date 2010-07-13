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
        filename = "cv.pdf"
        f = file(filename, "wb")
        pdf_template = ViewPageTemplateFile('pdf-view.pt')(self)
        #response.setHeader('Content-Type', 'application/pdf')
        #response.setHeader('Content-Disposition', 'filename=isaw.pdf')
        pdf = pisa.CreatePDF(pdf_template.encode("UTF-8"), f)
        f.close()
        response.redirect(self.context.absolute_url())
        if not pdf.err:
            pisa.startViewer(filename)
            print self.context.absolute_url()
