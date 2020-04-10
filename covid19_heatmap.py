from __future__ import print_function
from math import pi
import pandas as pd
import flask

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure

import pandas as pd
import geopandas as gpd

from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
import json


#def json_data(selectedYear):
def json_data():
    #yr = selectedYear
    df_yr = df[df['year'] == 2018]
    merged = gdf.merge(df_yr, left_on = 'state_code', right_on = 'state_code', how = 'left')
    merged.fillna('No data', inplace = True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data

def make_heatmap_object():
	shapefile = 'data/tl_2017_us_state.shp'
	datafile = 'data/usa_state_covid.csv'

	gdf = gpd.read_file(shapefile)[['STUSPS', 'NAME', 'geometry']]
	gdf.columns = ['state_code', 'state', 'geometry']
	#gdf = gdf[gdf['state_code'] == 'IL']
	gdf.drop( gdf[ gdf['state_code'] == 'AK' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'VI' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'PR' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'HI' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'MP' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'AS' ].index , inplace=True)
	gdf.drop( gdf[ gdf['state_code'] == 'GU' ].index , inplace=True)



	# In[2]:


	df = pd.read_csv(datafile, names = ['entity', 'state_code', 'year', 'count'], skiprows = 1)


	# In[3]:


	df_2016 = df[df['year'] == 2018]



	# In[4]:


	#Perform left merge to preserve every row in gdf.
	merged = gdf.merge(df_2016, left_on = 'state_code', right_on = 'state_code', how = 'left')

	#Replace NaN values to string 'No data'.
	merged.fillna('No data', inplace = True)



	#Read data to json
	merged_json = json.loads(merged.to_json())

	#Convert to str like object
	json_data = json.dumps(merged_json)

	#Input GeoJSON source that contains features for plotting.
	#geosource = GeoJSONDataSource(geojson = json_data(2018))
	geosource = GeoJSONDataSource(geojson=json_data())

	#Define a sequential multi-hue color palette.
	palette = brewer['YlGnBu'][8]

	#Reverse color order so that dark blue is highest obesity.
	palette = palette[::-1]

	#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
	color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40, nan_color = '#d9d9d9')

	#Define custom tick labels for color bar.
	tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

	#Add hover tool
	hover = HoverTool(tooltips = [ ('state','@state'),('count', '@count')])


	#Create color bar.
	color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
						 border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)


	#Create figure object.
	p = figure(title = 'Covid - 19 Cases', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None

	#Add patch renderer to figure.
	p.patches('xs','ys', source = geosource,fill_color = {'field' :'count', 'transform' : color_mapper},
			  line_color = 'black', line_width = 0.25, fill_alpha = 1)


	p.add_layout(color_bar, 'below')
	return p


app = flask.Flask(__name__)

@app.route("/")
def home_page():
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	heatmap = make_heatmap_object()
	script, div = components(heatmap)
	html = flask.render_template('embed_hm2.html',plot_script=script,plot_div=div,js_resources=js_resources,css_resources=css_resources)
	return encode_utf8(html)

if __name__ == "__main__":
	print(__doc__)
	app.run()

