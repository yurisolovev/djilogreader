import csv
import sys

from string import Template


head = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
     xmlns:gx="http://www.google.com/kml/ext/2.2"
     xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <Style id="flight">
        <LineStyle>
            <color>4a41a6</color>
            <width>4</width>
        </LineStyle>
        <LabelStyle>
            <scale>0</scale>
        </LabelStyle>
        <IconStyle>
            <Icon><href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href></Icon>
        </IconStyle>
    </Style>
    <Placemark>
        <name>Flight Route</name>
        <styleUrl>#flight</styleUrl>
        <gx:MultiTrack>
            <gx:Track>
                <altitudeMode>relativeToGround</altitudeMode>
"""

body = Template("""                <when>$time</when>
                <gx:angles>$yaw 0 0</gx:angles>
                <gx:coord>$long $lat $height</gx:coord>
""")


tail = """            </gx:Track>
        </gx:MultiTrack>
    </Placemark>
</Document>
</kml>"""


def generate_kml(csv_path, kml_path):
    with open(csv_path, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(kml_path, 'w') as kml:
            kml.write(head)
            for row in reader:
                kml.write(body.substitute({'time': '-'.join(row['CUSTOM.updateTime'].split('/')).replace(' ', 'T')+'Z',
                                           'long': row['OSD.longitude'],
                                           'lat': row['OSD.latitude'],
                                           'height': row['OSD.height'],
                                           'yaw': row['OSD.yaw']
                                           }))
            kml.write(tail)
    print('Done writing KML.', file=sys.stderr)
