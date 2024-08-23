import csv
import pandas as pd
import requests
import sys

# some website uri start with ttp (not "http")

# Needs revise: 
# https://omeka.soundingspirit.org/s/ssdl/item/1170
# https://omeka.soundingspirit.org/s/ssdl/item/1423

def get_coor(uri):
    # print(uri)
    # some uri are nan
    if uri == "nan":
        return "0,0"
    
    # some uri needs a "h" at the start
    if uri[0] == 't':
        uri='h'+uri
    
    # get the text
    mystr = requests.get(uri+".json").text

    # if the website has no coordinate information, return null
    if len(mystr.split('"value":')) == 1:
        return "0,0"
    
    # return the coordinate
    coor = mystr.split('"value":')[1].split("[")[1].split("]")[0]
    return coor

df = pd.read_csv('location.csv')

# longitude and latitude dictionary
long = []
lati = []

# rename columns and define types
df=df.rename(columns={"ssdl:pid": "PID", "ssdl:placeOfContributorAffiliation": "location", "ssdl:dateOfPublication": "Date"})
df["location"]=df["location"].astype(str)
df["Date"]=df["Date"].astype(str)
df["ssdl:placeOfContributorAffiliationUri"]=df["ssdl:placeOfContributorAffiliationUri"].astype(str)

# for each row, get the 
for x in df.index:
    progress = x/1299
    sys.stdout.write(f"\rProgress: {progress:05.1%}")
    sys.stdout.flush()
    # print(df.loc[x, "PID"])

    # collect latitude and longitude
    long_cur = ""
    lati_cur = ""
    df.loc[x, "location"]=df.loc[x, "location"].replace("\n",";")
    df.loc[x, "ssdl:placeOfContributorAffiliationUri"]=df.loc[x, "ssdl:placeOfContributorAffiliationUri"].replace("\n",";")
    for uri in df.loc[x, "ssdl:placeOfContributorAffiliationUri"].split(";"):
        coor = get_coor(uri)
        long_cur=long_cur+";"+coor.split(",")[0]
        lati_cur=lati_cur+";"+coor.split(",")[1]
    long.append(long_cur[1:])
    lati.append(lati_cur[1:])

    # remove the question mark in date
    df.loc[x,"Date"] = df.loc[x,"Date"].replace("?","")

df['Long'] = long
df['Lati'] = lati
df = df.drop('ssdl:placeOfContributorAffiliationUri', axis=1)

df.to_csv("location_processed.csv",index=False, encoding="utf-8")