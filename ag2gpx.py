#/usr/bin/env python
# -*- coding: utf-8 -*-
""" Create gpx file from AutoGuard srt file """

import sys
from datetime import datetime, timezone, timedelta

CMD_PARAM_ERR="ag2gpx [from filename(srt)] [to filename(gpx)]"

TAG_TIME = "時刻:"
TAG_SPEED = "スピード:"
TAG_LAT = "緯度:"
TAG_LNG = "経度:"

GPX_HEADER = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     version="1.1"
     creator="ag2gpx"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
<trk>
<trkseg>
"""[1:]
GPX_FOOTER = """
</trkseg>
</trk>
</gpx>
"""[1:]
GPX_TRKPT_FORMAT ="""
<trkpt lat="{lat}" lon="{lng}">
<time>{time}</time>
<desc>Spped: {speed} km/h</desc>
</trkpt>
"""[1:]

def main_routine():
    """main routine"""
    args = sys.argv
    if len(args) != 3:
        print(CMD_PARAM_ERR)
        sys.exit()
    from_filename = args[1]
    to_filename = args[2]

    with open(from_filename, "r") as from_file:
        from_lines = from_file.readlines()
    
    with open(to_filename, "w") as to_file:
        to_file.write(GPX_HEADER)

        point = {}
        for line in from_lines:
            line = line.strip()

            if TAG_TIME in line:
                time_string = line[len(TAG_TIME):].strip()
                jst = timezone(timedelta(hours=+9), 'JST')
                dt =  datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S") \
                        .replace(tzinfo=jst) \
                        .astimezone(timezone.utc)
                point['time'] = dt.isoformat()

            if TAG_SPEED in line:
                point['speed'] = line[len(TAG_SPEED):].strip()

            if TAG_LAT in line:
                point['lat'] = line[len(TAG_LAT):].strip()

            if TAG_LNG in line:
                point['lng'] = line[len(TAG_LNG):].strip()
                trkpt = GPX_TRKPT_FORMAT.format(**point)
                to_file.write(trkpt)
                point = {}

        to_file.write(GPX_FOOTER)

# main
main_routine()
