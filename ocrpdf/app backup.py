# importing modules 
import io
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas 
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
  
# initializing variables with values 
#image to pdf library
# fileName = '1926-Nakcok-UTL-0224'
fileName = '1922-Bethle-MTS-0004'
packet = io.BytesIO()
pdf = canvas.Canvas(packet, pagesize=letter)

# read your existing PDF
existing_pdf = PdfReader(open(fileName+'.pdf', "rb"))
box = existing_pdf.pages[0].mediabox
print(box)

with open(fileName+'.jpg.alto.xml', 'r') as f:
    data = f.read()
# print(data)
Bs_data = BeautifulSoup(data, "xml")
tokens = Bs_data.find_all('String')
pageheight = int(data.split('HEIGHT="')[1].split('"')[0]) # the height of the page
pagewidth = int(data.split('WIDTH="')[1].split('"')[0]) # the width of the page
pdfheight=float(box.height)
pageheight=3227
pdfwidth = float(box.width)
pagewidth=2134
scalefactor = pdfheight/pageheight
pdf.setPageSize((pdfwidth, pdfheight))
print(pdfwidth,pdfheight)
print(pagewidth,pageheight)
print(scalefactor)

# see if the words can be transparent

for token in tokens:
    text = str(token).split('CONTENT="')[1].split('"')[0]
    points = str(token).split('POINTS="')[1].split('"')[0].split(" ")
    left = int(points[0].split(',')[0])*scalefactor
    up = pdfheight-int(points[0].split(',')[1])*scalefactor
    right = int(points[1].split(',')[0])*scalefactor
    down = pdfheight-int(points[2].split(',')[1])*scalefactor
    width = right-left
    height = down-up
    # print(left, right, up, down,width,height,text)
    pdf.setFillColorRGB(1,1,1) # set fill(background) color to white
    pdf.setFont("Helvetica", (0-height))
    pdf.rect(left,up,width,height,fill=1) 
    pdf.setFillColorRGB(0,0,0) # set fill(background) color to black
    pdf.drawCentredString(left+width/2, down, text) 

pdf.save()
# creating the title by setting it's font  
# and putting it on the canvas 


#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)

output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
output_stream = open("destination.pdf", "wb")
output.write(output_stream)
output_stream.close()
