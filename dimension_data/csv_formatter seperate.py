import pandas as pd
import csv

def clean(text):
#   print("text:",text)
  res = ""
  flag = 1
  for char in text:
    if char.isdigit():
      res=res+char
    elif flag and (char == ',' or char == '.' or char == ';'):
      res=res+'.'
      flag=0
    else:
    #    print("res",res)
       return res
#   print("res",res)
  return res

df = pd.read_csv('Sounding Spirit dimension data - All.csv')

# interpret the width column and height column as strings
df['WIDTH'] = df['WIDTH'].astype(str)
df['HEIGHT'] = df['HEIGHT'].astype(str)

# drop the last column (which indicates where the data is from)
df = df.drop('FROM', axis=1)

# drop the line if there is no number in width or height
for x in df.index:
  if not any(char.isdigit() for char in df.loc[x, "WIDTH"]):
    df.drop(x, inplace = True)
for x in df.index:
  if not any(char.isdigit() for char in df.loc[x, "HEIGHT"]):
    df.drop(x, inplace = True)

# clean the width and height
for x in df.index:
    df.loc[x, "WIDTH"] = clean(df.loc[x, "WIDTH"])
    df.loc[x, "HEIGHT"] = clean(df.loc[x, "HEIGHT"])

# combine width and height and drop teh two columns
# df['DIMENSION'] = df['WIDTH'] + ' x ' + df['HEIGHT'] + " cm"
# df = df.drop('WIDTH', axis=1)
# df = df.drop('HEIGHT', axis=1)
values=df.values

file = open('PID_change.csv', mode ='r', encoding="utf-8" )
for line in file:
  tokens = line.split(",")
  if tokens[1] == 'New PID':
    continue
  # print(line)
  # print(line[0],line[1], end = ' ')
  if tokens[1] not in values:
    if tokens[0] in values:
      print("not changed:", tokens[0],tokens[1])
    elif not tokens[1].endswith("EMU") and not tokens[1].endswith("BRU"):
      print("not collected: ", tokens[1])
  df=df.replace(tokens[0],tokens[1])


df.to_csv('dimension_data_seperate.csv', index=False)