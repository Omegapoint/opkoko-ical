#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[application description here]"""

__appname__ = "OPKOKO 16.1 Cal"
__author__  = "Jakob Petersson"
__version__ = "0.1"
__license__ = "GNU GPL 3.0 or later"

import json

class Calendar:
    'Calendar'

    def __init__(self, filename, calendarName):
        self.calendarName = calendarName
        self.file = open(filename, 'w')
        self.calData = ''
        
    def begin(self):
        self.calData += (
            "BEGIN:VCALENDAR\n"
            "METHOD:PUBLISH\n"
            "VERSION:2.0\n"
            "X-WR-CALNAME:" + self.calendarName + "\n"
            "PRODID:-//Apple Inc.//Mac OS X 10.11.5//EN\n"
            "X-APPLE-CALENDAR-COLOR:#1BADF8\n"
            "X-WR-TIMEZONE:Europe/Stockholm\n"
            "CALSCALE:GREGORIAN\n"

            "BEGIN:VTIMEZONE\n"
            "TZID:Europe/Madrid\n"

            "BEGIN:DAYLIGHT\n"
            "TZOFFSETFROM:+0100\n"
            "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\n"
            "DTSTART:19810329T020000\n"
            "TZNAME:CEST\n"
            "TZOFFSETTO:+0200\n"
            "END:DAYLIGHT\n"

            "BEGIN:STANDARD\n"
            "TZOFFSETFROM:+0200\n"
            "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\n"
            "DTSTART:19961027T030000\n"
            "TZNAME:CET\n"
            "TZOFFSETTO:+0100\n"
            "END:STANDARD\n"

            "END:VTIMEZONE\n")

    def addEvent(self, start, end, summary, location, description):
        self.calData += (
            "BEGIN:VEVENT\n"
            "TRANSP:OPAQUE\n"
            "X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\n"
            "DTSTART;TZID=Europe/Madrid:" + start + "\n"
            "DTEND;TZID=Europe/Madrid:" + end + "\n"
            "SUMMARY:" + summary + "\n"
            "LOCATION:" + location + "\n"
            "DESCRIPTION:" + description + "\n"
            "END:VEVENT\n")

    def end(self):
        self.calData += ("END:VCALENDAR\n")

    def write(self):
        self.file.write(self.calData)
        self.file.close()

class OpkokoJsonParser:
    'OPKOKO JSON Parser'

    def __init__(self, filename):
        jsonFile = open(filename, 'r')
        self.jsonData = json.load(fp=jsonFile, encoding="utf-8")

        self.calendar = Calendar("opkoko.ics", "OPKOKO 16.1")
        self.calendar.begin()

        for talk in self.jsonData['talks']:
            self._parseTalk(talk)
            
        self.calendar.end()
        self.calendar.write()

    def _parseTalk(self, talk):
        begin = talk['begin']
        end = talk['end']
        summary = talk['name']
        location = '' if 'location' not in talk else talk['location']

        description = ''
        if 'description' in talk:
            description += talk['description'] + "\\n"
        if 'speaker' in talk:
            description += "\\nTalare: " + talk['speaker'] + "\\n"
        if 'targetAudience' in talk:
            description += "Målgrupp: " + talk['targetAudience'] + "\\n"

        self.calendar.addEvent(begin, end, summary, location, description)

# -- Code Here --
def main():
    par = OpkokoJsonParser("opkokoCal.json")

if __name__ == '__main__':
    main()