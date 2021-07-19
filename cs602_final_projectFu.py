import csv
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pydeck as pdk


def df_map(locations):
  df = pd.DataFrame(locations, columns=["Building", "lat", "lon"])
  st.title("100 Tallest Buildings of the World")
  layer1 = pdk.Layer('ScatterplotLayer',
                       data = df,
                       get_position = '[lon, lat]',
                       get_radius = 6000,
                       get_color = [0,0,255,60],
                       pickable = True)
    
  tool_tip = {"html": "Building Name:<br/> <b>{Building}</b>",
                "style": { "backgroundColor": "steelblue",
                          "color": "white"}}
    
  return pdk.Deck(
        map_style = 'mapbox://styles/mapbox/light-v9',
        initial_view_state = pdk.ViewState(
            latitude = 0,
            longitude = 0,
            zoom = 1,
            pitch = 10),
            layers = [layer1],
            tooltip = tool_tip)


def pie_chart(total, collectionList):
  st.title("The Percentage Structural Materials")

  values = [] 
  for material in collectionList:
    count = 0
    for row in total[1:]:
      if row[11] == material:
        count += 1
    values.append(count/(len(total) - 1))
  plt.pie(values, labels = collectionList, autopct = '%1.1f%%',shadow = True)
  plt.axis('equal')
  return plt


def main():
  locations = []
  maxYear = 0
  minYear = 2022
  totalData = []
  materialSet = set()
  yearSet = set()
  with open('Skyscrapers2021.csv', 'r') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
      totalData.append(row)
      if row[0] == "RANK":
        continue
      maxYear = max(maxYear, int(row[6]))
      minYear = min(minYear, int(row[6]))
      yearSet.add(int(row[6]))
      materialSet.add(row[11])
      locations.append((row[1],float(row[4]),float(row[5])))


  x = st.slider("Select Year", minYear, maxYear, minYear)
  st.write('You selected the year ', x, ' !')
  names = []
  city = []
  addresses = []
  lat = []
  lon = []
  mat = []
  displayDict = {"Name":names, "City":city,"Full Address":addresses,"Latitude":lat,"Longitude":lon,"MATERIAL":mat}
  for row in totalData:
    if row[0] == "RANK":
      continue
    if x == int(row[6]):
      names.append(row[1])
      city.append(row[2])
      addresses.append(row[3])
      lat.append(row[4])
      lon.append(row[5])
      mat.append(row[11])
  df = pd.DataFrame(displayDict)
  df


  materialList = list(materialSet)
  material = st.radio("Select the material type",materialList)
  materialDisplay = {"Rank":[], "City":[],"Full Address":[],"Link":[]}


  for row in totalData:
    if row[0] == "RANK":
      continue
    if material == row[11]:
      materialDisplay["Rank"].append(row[0])
      materialDisplay["City"].append(row[2])
      materialDisplay["Full Address"].append(row[3])
      materialDisplay["Link"].append(row[-1])
  material_df = pd.DataFrame(materialDisplay)
  material_df


  st.pyplot(pie_chart(totalData, materialList))
  st.pydeck_chart(df_map(locations))

main()
