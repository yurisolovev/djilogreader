import csv
import sys

from string import Template


head = Template("""<?xml version="1.0"?>
<gpx version="1.1" creator="GDAL 2.2.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogr="http://osgeo.org/gdal" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
<metadata><bounds minlat="$min_lat" minlon="$min_long" maxlat="$max_lat" maxlon="$max_long"/></metadata>                  
<trk>
  <name>GPS-трек полета</name>
  <extensions>
    <ogr:begin>$start_time</ogr:begin>
    <ogr:end>$end_time</ogr:end>
  </extensions>
  <trkseg>
""")

body = Template("""    <trkpt lat="$lat" lon="$long">
    </trkpt>
""")

tail = """  </trkseg>
</trk>
</gpx>
"""


def generate_gpx(csv_path, gpx_path):
    lat = []
    long = []
    start_time = ''
    end_time = ''

    with open(csv_path, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            long.append(row['OSD.longitude'])
            lat.append(row['OSD.latitude'])
            start_time = row['DETAILS.timestamp']
            end_time = row['CUSTOM.updateTime']
        min_lat = min(lat)
        min_long = min(long)
        max_lat = max(lat)
        max_long = max(long)

        with open(gpx_path, 'w') as gpx:
            gpx.write(head.substitute({'start_time': start_time + '+00',
                                       'end_time': end_time + '+00',
                                       'min_lat': min_lat,
                                       'min_long': min_long,
                                       'max_lat': max_lat,
                                       'max_long': max_long
                                       }))
            for _ in range(len(lat)):
                gpx.write(body.substitute({'lat': lat[_],
                                           'long': long[_]
                                           }))
            gpx.write(tail)
    print('Done writing GPX.', file=sys.stderr)
