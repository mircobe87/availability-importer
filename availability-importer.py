from __future__ import print_function

import datetime
import os.path
import shift_reader
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from progress.bar import ChargingBar

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']

def get_calendar(gc_service, calendar_name):
    list_result = gc_service.calendarList().list().execute()
    calendars = list_result.get('items', [])
    out_calendar = None
    for calendar in calendars:
        if calendar['summary'] == calendar_name:
            out_calendar = calendar
    return out_calendar

def fetch_events(gc_service, calendar, timeMin, timeMax):
    events_result = gc_service.events().list(
        calendarId=calendar['id'],
        timeMin=timeMin.isoformat(),
        timeMax=timeMax.isoformat(),
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def delete_events(gc_service, calendar, events):
    bar = ChargingBar('Deleting', max=len(events))
    for e in events:
        gc_service.events().delete(calendarId=calendar['id'], eventId=e['id'], sendUpdates='none').execute()
        bar.next()
    bar.finish()
    print("All events removed")

def get_involved_time_range(availability):
    min_start_datetime = None
    max_end_datetime = None
    for item in availability:
        min_start_datetime = item['start'] if min_start_datetime is None or min_start_datetime > item['start'] else min_start_datetime
        max_end_datetime = item['end'] if max_end_datetime is None or max_end_datetime < item['end'] else min_start_datetime
    return min_start_datetime, max_end_datetime

def load_availability(gc_service, calendar, availability):
    bar = ChargingBar('Saving', max=len(availability))
    for a in availability:
        gc_service.events().insert(
            calendarId=calendar['id'],
            sendNotifications='none',
            body={
                'summary': a['name'],
                'start': {
                    'dateTime': a['start'].isoformat()
                },
                'end': {
                    'dateTime': a['end'].isoformat()
                }
            }
        ).execute()
        bar.next()
    bar.finish()
    print("All {} events created".format(len(availability)))


def main(args_namespace):
    
    CALENDAR_NAME = args_namespace.calendar
    AVAILABILITY_FILE = args_namespace.event_file
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Search target calendar by name
        calendar = get_calendar(service, CALENDAR_NAME)
        if calendar is None:
            raise Exception("No calendar found with name {}".format(CALENDAR_NAME))
        print("Target calendar: {} ({})".format(calendar['summary'], calendar['id']))

        # Load availability from file
        availability_items = shift_reader.read_availability(AVAILABILITY_FILE)
        minTime, maxTime = get_involved_time_range(availability_items)
        print("Read {} items from file '{}'".format(len(availability_items), AVAILABILITY_FILE))
        print("Time range: {} - {}".format(minTime.isoformat(), maxTime.isoformat()))

        # Call API to fetch alredy saved events
        events = fetch_events(service, calendar, minTime, maxTime)

        if not events:
            print('No availability found in this time range')
        else:
            print('Found {} items already saved in calendar'.format(len(events)))
            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                print("{} - {}: {}".format(start, end, event['summary'] if 'summary' in event else 'No Title'))
            remove = None
            while remove is None:
                print("All those items will be removed. Continue? (y/N): ", end='')
                in_str = input().strip()
                if len(in_str) == 0 or in_str.lower() == 'n':
                    remove = False
                elif in_str.lower() == 'y':
                    remove = True
                else:
                    print("No valid value. Please put only 'y' or 'n'.")
            if remove:
                delete_events(service, calendar, events)

        load_availability(service, calendar, availability_items)

    except HttpError as error:
        print('An error occurred: %s' % error)

parser = argparse.ArgumentParser(description='Load availability in google calendar.')
parser.add_argument('-c', '--calendar', metavar='CALENDAR_NAME', help='the name of calendar where you want to upload events.', action='store', required=False, default='Reperibilità')
parser.add_argument('event_file', metavar='EVENT_FILE', help='the CSV file coniainig event to upload.')

if __name__ == '__main__':
    main(parser.parse_args())