#!/bin/env python3

# imports
import argparse
from icalendar import Calendar, Event, vCalAddress, vText
#from datetime import datetime
from pathlib import Path
import sys
#import pytz

# helper
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# argument parsing
parser = argparse.ArgumentParser(description = 'Cleans up a calendar file provided by the GfA',
                                 epilog = 'https://github.com/carstene1ns/abfuhr-clean')
parser.add_argument('-o', '--output', type=Path, help='Output file name, if not provided, will be output to stdout')
parser.add_argument('-v', '--verbose', action='store_true', help='Display raw calendar events on stderr')
parser.add_argument('input', type=Path, help='The ical/.ics file to clean up')
args = parser.parse_args()


# load calendar
with open(args.input, 'rb') as f:
	cal = Calendar.from_ical(f.read())

# convert 
for item, component in enumerate(cal.walk(name = "vevent"), start=1):
	# remove junk
	del component['url']
	del component['location']
	del component['description']
	del component['priority']

	# fixup summary
	s = component['summary']

	# remove space at end
	s = vText(s.strip())
	# correct umlauts "muell" -> "müll"
	s = vText(s.replace('ue', 'ü'))
	# set language
	s.params['language'] = vText('de')

	component['SUMMARY'] = s

	# debug
	if args.verbose:
		eprint("Event number", item)
		eprint('-' * 20)
		eprint(component.to_ical().decode("utf-8").replace('\r\n', '\n').strip())
		eprint('-' * 60 + '\n')

# add reminder to update


# output
if args.output:
	with open(args.output, 'wb') as f:
		f.write(cal.to_ical())
else:
	print(cal.to_ical().decode("utf-8"))
