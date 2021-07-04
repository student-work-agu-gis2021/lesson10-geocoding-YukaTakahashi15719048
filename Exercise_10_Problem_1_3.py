#!/usr/bin/env python
# coding: utf-8

# ## Problem 1: Geocode shopping centers
# 
# In problem 1 the task is to find out the addresses for a list of shopping centers and to geocode these addresses in order to represent them as points. The output should be stored in a Shapefile called `shopping_centers.shp` 
# 

# Import modules
import geopandas as gpd
import pandas as pd
# Read the data (replace "None" with your own code)
fp  = 'shopping_centers.txt'
data = pd.read_table(fp, sep=';', header=None)

# YOUR CODE HERE 1 to read the data
data.columns=['id','name', 'addr']

#TEST COEE
# Check your input data
print(data)

# - Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`:

# Geocode the addresses using Nominatim
geo = None
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
#YOUR CODE HERE 2 for geocoding
geo = geocode(data['addr'], provider='nominatim', user_agent='application name')


#TEST CODE
# Check the geocoded output
print(geo)

#TEST CODE
# Check the data type (should be a GeoDataFrame!)
print(type(geo))


# Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into JGD2011** (EPSG:6668):

# YOUR CODE HERE 3 to set crs.
from pyproj import CRS
geo = geo.to_crs(CRS.from_epsg(6668))
geodata = geo.join(data)

#TEST CODE
# Check layer crs
print(geo.crs)


# YOUR CODE HERE 4 to join the tables
geodata = geo.join(data)

#TEST CODE
# Check the join output
print(geodata.head())


# - Save the output as a Shapefile called `shopping_centers.shp` 

# Define output filepath
out_fp = None
# YOUR CODE HERE 5 to save the output
fp = 'shopping_centers.shp'
geo.to_file(fp)

# TEST CODE
# Print info about output file
print("Geocoded output is stored in this file:", out_fp)


# ## Problem 2: Create buffers around shopping centers
# 
# Let's continue with our case study and calculate a 1.5 km buffer around the geocoded points. 
 

# YOUR CODE HERE 6 to create a new column
geodata['buffer']=None

# YOUR CODE HERE 7 to set buffer column
geodata['buffer'] = geodata['geometry'].buffer(distance=1500)

#TEST CODE
print(geodata.head())

#TEST CODE
# Check the data type of the first value in the buffer-column
print(type(geodata.at[0,'buffer']))


#TEST CODE
# Check the areas of your buffers in km^2
print(round(gpd.GeoSeries(geodata["buffer"]).area / 1000000))


# - Replace the values in `geometry` column with the values of `buffer` column:

# YOUR CODE HERE 8 to replace the values in geometry
geodata['geometry'] = geodata['buffer']

#TEST CODE
print(geodata.head())


# ## Problem 3: How many people live near shopping centers? 
# 
# Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. 
# 

# YOUR CODE HERE 9
# Read population grid data for 2018 into a variable `pop`.
import requests 
import geojson
url = 'https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-mesh500h30.html#prefecture13'
params = dict(service='WFS',version='2.0.0',request='GetFeature',
              typeName='500m_mesh_2018_13.shp',outputFormat='json')
r = requests.get(url, params=params)
pop = gpd.GeoDataFrame.from_features(geojson.loads(r.content))

pop = pop[[ 'geometry','PTN_2020' ]]
pop.crs = CRS.from_epsg(4612).to_wkt()
geodata = geodata.to_crs(pop.crs)

#TEST CODE
# Check your input data
print("Number of rows:", len(pop))
print(pop.head(3))


# In[ ]:


# Create a spatial join between grid layer and buffer layer. 
# YOUR CDOE HERE 10 for spatial join
join = gpd.sjoin(geodata, pop, how="inner", op="intersects")


# YOUR CODE HERE 11 to report how many people live within 1.5 km distance from each shopping center
grouped = join.groupby('name')
for i, group in grouped:
    print('store: ', i,'  ; population:', sum(group['PTN_2020']))

# **Reflections:**
#     
# - How challenging did you find problems 1-3 (on scale to 1-5), and why?
# - What was easy?
# - What was difficult?

# YOUR ANSWER HERE

# Well done!
