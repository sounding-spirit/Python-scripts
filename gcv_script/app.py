import requests
import json
import base64
import os
import sys
import click
import google.auth.transport.requests
import google.oauth2.service_account as service_account
from PIL import Image

# set up some initial variables
url = f'https://vision.googleapis.com/v1/images:annotate'

json_file_path = 'request.json' # Path to request json
gcv_output_path = 'temp.json' # Path to the gcv output file
hocr_output_path = "temp.hocr" # Path to the hocr output file

# get access token
credentials = service_account.Credentials.from_service_account_file(
    'precise-duality-432316-k8-71b151d9db35.json', # change this to the key file
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
request = google.auth.transport.requests.Request()
credentials.refresh(request)

# transform alto 4.0 to alto 4.2
def transform(image_path, ocr_folder_path,xml_path):
    xml_file = open(xml_path,"r+")
    text = xml_file.read()
    xml_file.close()

    # if the data is not read successfully, rerun the ocr
    if 'HEIGHT="0" WIDTH="0" VPOS="0" HPOS="0"/>' in text: 
        print("Error happened when ocring "+image_path+", rerunning...")
        ocr(image_path,ocr_folder_path)
        return
    
    xml_file = open(xml_path,"r+")
    text = text.replace("ComposedBlock","TextBlock")
    blocks = text.split("<String")
    text = blocks[0]
    for x in range(1,len(blocks),1):
        block = blocks[x]
        leng = len(block.split("/>")[0])+2
        height = int(block.split('HEIGHT="')[1].split('"')[0])
        width = int(block.split('WIDTH="')[1].split('"')[0])
        left = int(block.split('HPOS="')[1].split('"')[0])
        top = int(block.split('VPOS="')[1].split('"')[0])
        right = left+width
        down = top + height
        content = block.split('CONTENT="')[1].split('"')[0]
        block = '<String HEIGHT="'+str(height)+'" WIDTH="'+str(width)+'" HPOS="'+str(left)+'" VPOS="'+str(top)+'" CONTENT="'+content+'"><Shape><Polygon POINTS="'+str(left)+','+str(top)+' '+str(right)+','+str(top)+' '+str(right)+','+str(down)+' '+str(left)+','+str(down)+'" /></Shape></String>'+block[leng:]
        text=text+block

    xml_file.seek(0)
    xml_file.write(text)
    xml_file.truncate() # truncate the file in case the original file is larger than the written text
    xml_file.close()

# ocr the image and write the result (in alto) to out_path
def ocr(image_path, ocr_folder_path):
    print("Checking image: "+image_path)

    # Read the JSON data from the file
    json_file = open(json_file_path, 'a')
    json_file.write('{"requests":[{"image":{"content":"')
    json_file = open(json_file_path, 'ab')
    image = open(image_path, 'rb')
    json_file.write(base64.b64encode(image.read()))
    json_file = open(json_file_path, 'a+')
    json_file.write('"},"features":{"type":"DOCUMENT_TEXT_DETECTION","maxResults":1},"imageContext":{"languageHints":"en"}}]}')
    json_file.seek(0)

    # Set up the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + credentials.token
    }
    # Make the POST request
    response = requests.post(url, headers=headers, data=json_file.read(), verify=False)  # verify=False is equivalent to -k in curl
    json_file.close()
    os.remove(json_file_path)

    # print("response:",response.json())
    # Save the response to a file
    gcv_output = open(gcv_output_path, 'w')
    json.dump(response.json(),gcv_output)
    gcv_output.close()

    # get width and height of image
    im = Image.open(image_path)
    width, height = im.size

    # transform gcv to hocr using gcv2hocr from github
    gcv2hocr_cmd = "py gcv2hocr.py --savefile "+hocr_output_path+" --page-width "+str(width)+" "+" --page-height "+str(height)+" "+gcv_output_path
    # print(gcv2hocr_cmd)
    os.system(gcv2hocr_cmd)
    os.remove(gcv_output_path)

    # transform hocr to alto 4.0 using saxon
    xml_path = os.path.join(ocr_folder_path, os.path.split(image_path)[1].split(".")[0]+".xml")
    hocr2alto_cmd = "java -jar saxon-he-12.5.jar -s:temp.hocr -xsl:hocr__alto4.xsl -o:"+xml_path
    # print(hocr2alto_cmd)
    os.system(hocr2alto_cmd)
    os.remove(hocr_output_path)

    # transform the alto 4.0 to alto 4.2
    transform(image_path, ocr_folder_path,xml_path)

# cli method
@click.argument("image_folder_path", type=click.Path(dir_okay=True, exists=True))
@click.argument("ocr_folder_path", type=click.Path(dir_okay=True, exists=True))
def cli(image_folder_path, ocr_folder_path):
    # image_folder_path = "C:/gcv_script/gcv/images"
    # ocr_folder_path = "C:/gcv_script/gcv/ocr"
    for image_path in os.listdir(image_folder_path):
        ocr(os.path.join(image_folder_path,image_path),ocr_folder_path)

if __name__=="__main__":
    cli(sys.argv[1],sys.argv[2])