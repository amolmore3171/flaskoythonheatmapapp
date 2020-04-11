from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import io
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = Flask(__name__)


@app.route('/plot.png')
def home_page():
  chicagoland_agg_datafile='data/Chicagoland_agg.csv'
  Chicagoland_agg = pd.read_csv(chicagoland_agg_datafile, names=['county', 'date_str', 'num_events_by_county', 'num_devices_by_county','avg_events_by_county'], skiprows=1)


  fig, ax = plt.subplots(figsize=(22,8))
  for c in list(Chicagoland_agg.county.unique()):
    ax.plot(Chicagoland_agg[Chicagoland_agg['county']==c]['avg_events_by_county'], marker='.', linestyle='-', linewidth=0.5, label=c)

  ax.set_ylabel('Avg. # Events')
  ax.set_title('GDO Open and Close Events: Chicagoland, Jan - Apr 2020')
  plt.legend()
  #-------------------------------------------
  # Set x-axis major ticks to weekly interval, on Mondays
  ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
  # Format x-tick labels as 3-letter month name and day number
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
  #--------------------------------------------

  ax.set_ylim((3,14))
  ax.set_yticks(range(3,14))

  ax.grid('x', ls=':')


  plt.axvline("2020-03-16", color="blue", linestyle='--', linewidth=0.5)
  plt.axvline("2020-03-21", color="red", linestyle='--', linewidth=0.5)


  canvas = FigureCanvas(fig)
  output = io.BytesIO()
  canvas.print_png(output)
  response = make_response(output.getvalue())
  response.mimetype = 'image/png'
  return response


if __name__ == '__main__':
  print(__doc__)
  app.run()
