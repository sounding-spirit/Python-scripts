# import libraries
import pandas as pd
import io
import sys
import os.path
import geopy
import folium
import urllib.request
import csv

df = pd.read_csv('location_processed.csv')
df['location'] = df['location'].astype(str)
df['ssdl:shortTitle'] = df['ssdl:shortTitle'].astype(str)

object=geopy.Nominatim(user_agent="Nikki")
center=object.geocode("Atlanta, GA")
map = folium.Map(location=[center.latitude,center.longitude], zoom_start=4)


def get_url(PID):

  # get the omeka website html
  fp = urllib.request.urlopen("https://omeka.soundingspirit.org/s/ssdl/index/search?fulltext_search="+PID)
  mybytes = fp.read()
  mystr = mybytes.decode("utf8")
  fp.close()

  # parse the html to get the link to the songbook
  link=mystr.split('<a class="resource-link" href=')[1].split('"')[1].replace("&#x3A;",":").replace("&#x2F;","/")
  return link

if not os.path.isfile('PID2link.csv'):
  csvfile = open('PID2link.csv', 'w', newline='', encoding='utf-8')
  writer = csv.writer(csvfile, delimiter=',',
                      quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["PID","link"])
  for x in df.index:
    progress = x/1299
    sys.stdout.write(f"\rInitializing... ({progress:05.1%})") # progress bar
    sys.stdout.flush()
    link = get_url(df.loc[x, "PID"])
    writer.writerow([df.loc[x, "PID"],link])

dict = {}

df2 = pd.read_csv('PID2link.csv')
for x in df.index:
  location = df.loc[x, "location"].split(";")
  lo = df.loc[x, "Long"].split(";")
  la = df.loc[x, "Lati"].split(";")
  link = df2.loc[x,"link"]
  for i in range (0,len(location)):
    if i>=len(lo) and i>=len(la):
      lo.append(0)
      la.append(0)
    if lo[i] == 0 and la[i] == 0:
      if location[i] == "Dale City, PA":
        lo[i] = -77.342350
        la[i] = 38.648284
        continue
      if location[i] == '':
        continue
      # print("location:",location[i])
      loc = object.geocode(location[i])
      lo[i] = loc.longitude
      la[i] = loc.latitude
    coor = str(lo[i])+";"+str(la[i])
    if coor not in dict:
      dict[coor]='<a>'+location[i]+'</a>'
    dict[coor]=dict[coor]+"<br><a href='https://omeka.soundingspirit.org"+link+"'>"+df.loc[x, "ssdl:shortTitle"]+'</a>'

df3=pd.DataFrame(dict.items())
long = []
lati = []
desc = []
leng = []
for x in df3.index:
  coor = df3.loc[x,0]
  long.append(coor.split(";")[0])
  lati.append(coor.split(";")[1])
  d = df3.loc[x,1]
  l = len(df3.loc[x,1].split("<br>"))-1
  if l > 3:
    d = '''
    <div id="hover-div">
      '''+d.split("<br>")[0]+"<br>"+d.split("<br>")[1]+"<br>"+d.split("<br>")[2]+'''<br>
      <button id='button' style='background:none; border:none;color:blue;text-decoration:underline;'>more details</button>
      <script></script>
    </div>'''
  desc.append(d)
  leng.append(l)
df3["Long"]=long
df3["Lati"]=lati
df3["Desc"]=desc
df3["Leng"]=leng
df3.drop(0, axis=1)
df3.to_csv("location_coor.csv",index=False)

for x in df3.index:
  coor = df3.loc[x,0]
  lo=df3.loc[x,"Long"]
  la=df3.loc[x,"Lati"]
  folium.Marker([la,lo], popup=folium.map.Popup(html=df3.loc[x,"Desc"],max_width=200)).add_to(map)
  
map.save("index.html")