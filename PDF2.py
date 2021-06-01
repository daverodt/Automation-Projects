from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import os
import time
import argparse
import tempfile
import PyPDF2
import datetime
from reportlab.pdfgen import canvas
from pathlib import Path
from appJar import gui
from tkinter import messagebox

def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name

def sign_pdf(pdf, signature, page_num, x1, y1, width, height):
    #TODO: use a gui or something.... for now, just trial-and-error the coords
    #page_num, x1, y1, width, height = [int(a) for a in args.coords.split("x")]
    #page_num -= 1
    print(pdf)
    output_filename = str(pdf[:-4]) + " signed.pdf"

    pdf_fh = open(pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            # Create PDF for signature
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            c.drawImage(signature, x1, y1, width, height)
            
            c.showPage()
            c.save()

            # Merge PDF in to original page
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)

    with open(output_filename, 'wb') as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)
	
def openpdf(dirname):

	##Change Signature
	signature = 'C:\\Users\\DAVIDRODRIGUEZTORRES\\Downloads\\unnamed.png'
	for filename in os.listdir(dirname):
		#print()
		pdf_fh = dirname + "\\" + filename
		fp = open(pdf_fh, 'rb')
		rsrcmgr = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr, laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		pages = PDFPage.get_pages(fp)

		count = -1
		for page in pages:
		    count +=1
		    interpreter.process_page(page)
		    layout = device.get_result()
		    for lobj in layout:
		        if isinstance(lobj, LTTextBox):
		            x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
		            if "Liduvina" in text or "Rodriguez" in text:
		            	print('At %r is text: %s' % ((x, y), text))
		            	sign_pdf(pdf_fh,signature, count, x+80,y-5,80,25)
		            	
'''
def validate_inputs(input_folder):

	if not(Path(input_folder)).exists():
		errors = True
		error_msgs = "Please Select a valid output directory"
	else:
		errors = False
		error_msgs = ""

	return(errors, error_msgs)
​
​'''
def press(button):
    """ Process a button press
​
    Args:
        button: The name of the button. Either Process of Quit
    """
    if button == "Process":
        src_folder = app.getEntry("Output_Directory")
        #page_range = app.getEntry("Page_Ranges")
        #out_file = app.getEntry("Output_name")
        errors, error_msg = (False, "")#validate_inputs(src_folder)
        #print(errors)
        #print(error_msg)
        if errors:
        	print(errors)
        	app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
        	print("no errors")
        	Invoice = openpdf(src_folder)
        	#messagebox.showinfo(message="Los PDF se finalizaron Exitosamente", title="Finalizado Exitosamente")
        	app.infoBox("Finished without error", "The program runned correctly", parent=None)
        	app.stop()
    else:
    	app.stop()

if __name__ == '__main__':
	app = gui("Sign Invoices", useTtk=True)
	app.setTtkTheme("vista")
	app.setSize(500, 200)
	app.addLabel("Choose Source PDF Folder")
	app.addDirectoryEntry("Output_Directory")
	app.addButtons(["Process", "Quit"], press)
	app.go()
