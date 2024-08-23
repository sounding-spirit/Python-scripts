# importing modules 
import io
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas 
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
import click
import img2pdf
import os
import sys
from PIL import Image
  
# initializing variables with values 
#image to pdf library
# fileName = '1926-Nakcok-UTL-0224'
def pdf(image_path,xml_folder_path,pdf_folder_path):
    packet = io.BytesIO()
    pdf = canvas.Canvas(packet, pagesize=letter)
    filename = os.path.split(image_path)[1].split(".")[0]

    # create pdf background (by converting image to pdf)
    temp_pdf_path = "temp.pdf"
    pdf_bytes = img2pdf.convert(Image.open(image_path).filename)
    file = open(temp_pdf_path, "wb")
    file.write(pdf_bytes)
    file.close()

    image = open(temp_pdf_path,'rb')
    pdf_background = PdfReader(image)
    box = pdf_background.pages[0].mediabox

    with open(os.path.join(xml_folder_path,filename+'.xml'), 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    tokens = Bs_data.find_all('String')
    pageheight = int(data.split('HEIGHT="')[1].split('"')[0]) # the height of the page
    pagewidth = int(data.split('WIDTH="')[1].split('"')[0]) # the width of the page
    pdfheight=float(box.height)
    pdfwidth = float(box.width)
    scalefactor = pdfheight/pageheight
    pdf.setPageSize((pdfwidth, pdfheight))
    pdf.setFillColorRGB(1,1,1,0) # set fill color to white transparent

    for token in tokens:
        text = str(token).split('CONTENT="')[1].split('"')[0]
        points = str(token).split('POINTS="')[1].split('"')[0].split(" ")
        left = int(points[0].split(',')[0])*scalefactor
        up = pdfheight-int(points[0].split(',')[1])*scalefactor
        right = int(points[1].split(',')[0])*scalefactor
        down = pdfheight-int(points[2].split(',')[1])*scalefactor
        width = right-left
        height = down-up
        # pdf.setFillColorRGB(1,1,1) # set fill color to white 
        # pdf.rect(left,up,width,height,fill=1) 
        # pdf.setFillColorRGB(0,0,0) # set fill color to black
        pdf.setFont("Helvetica", (0-height))
        pdf.drawCentredString(left+width/2, down, text) 

    pdf.save()

    # create a new PDF with Reportlab
    packet.seek(0)
    new_pdf = PdfReader(packet)
    if new_pdf.is_encrypted:
        new_pdf.decrypt('')

    # add the new pdf on the existing page
    output = PdfWriter()
    page = pdf_background.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    image.close()
    os.remove(temp_pdf_path)

    # rite "output" to a real file
    pdf_path = os.path.join(pdf_folder_path,filename+".pdf")
    output_stream = open(pdf_path, "ab")
    output.write(output_stream)
    output_stream.close()
    print("PDF written to "+pdf_path)

@click.argument("image_folder_path", type=click.Path(dir_okay=True, exists=True))
@click.argument("xml_folder_path", type=click.Path(dir_okay=True, exists=True))
@click.argument("pdf_folder_path", type=click.Path(dir_okay=True, exists=True))
def cli(image_folder_path, xml_folder_path,pdf_folder_path):
    for image_path in os.listdir(image_folder_path):
        pdf(os.path.join(image_folder_path,image_path),xml_folder_path,pdf_folder_path)

if __name__=="__main__":
    cli(sys.argv[1],sys.argv[2],sys.argv[3])