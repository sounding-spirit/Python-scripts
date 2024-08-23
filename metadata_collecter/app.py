# import libraries
import urllib.request
import json
import csv
import sys

# get the data using the api
def get_page(index):
    # access the url
    fp = urllib.request.urlopen("https://omeka.soundingspirit.org/api/items?per_page=1&page="+str(index))
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    # get data
    data_json = json.loads(mystr)
    if len(data_json)==0:
        return []
    data=data_json[0]
    # print(data)

    # parse the data and get information
    res = []
    for parameter in parameters: # for each parameter we need
        value = ""
        if parameter not in data:
            res.append("")
            continue
        for token in data[parameter]:
            if value != "":
                value = value +";" # merge all info using ';'
            value = value + token['@value']
        res.append(value)
    # print(x)
    # print(res)
    return res
        
# hard code the parameters needed
parameters = ["ssdl:pid","ssdl:placeOfContributorAffiliation","ssdl:placeOfContributorAffiliationUri","ssdl:dateOfPublication","ssdl:shortTitle"]

# open csv file
csvfile = open('data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(parameters) # write first row

# for all entries
for x in range (0,1299,1):
    data = get_page(x)
    progress = x/1299
    sys.stdout.write(f"\rProgress: {progress:05.1%}") # progress bar
    sys.stdout.flush()
    if data==[]:
        exit
    writer.writerow(data) # write the data into csv

sys.stdout.write("\rFinished!        ")
sys.stdout.flush()