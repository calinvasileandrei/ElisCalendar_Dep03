from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar',"https://www.googleapis.com/auth/calendar.events"]
calendarID= "6esvbg4rdj44egpni2r65kohjs@group.calendar.google.com"


def getConn():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('credentials/token.pickle'):
        with open('credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds )
    return  service



def printEvents(service,resoultNumber=999999):
    # Call the Calendar API for events
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming',resoultNumber,' events')
    try:
        events_result = service.events().list(calendarId=calendarID,maxResults=resoultNumber, singleEvents=True,orderBy='startTime').execute()
    except:
        print(datetime.datetime.now()," Error getting events list !")

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'] ,"id:",event['id'])



def insertEvent(service,subject,startDateTime,endDateTime):
    event = { #setting up the obj event
        'summary': subject,
        'start': {
            'dateTime': startDateTime,
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': 'Europe/Rome',
        },
    }
    insEvent = True
    while insEvent == False:
        try:
            event = service.events().insert(calendarId=calendarID, body=event).execute()
            insEvent = True
        except:
            print(datetime.datetime.now(), " Error insert in calendar: ", calendarID, ": Event:", event)
            insEvent = False
            time.sleep(4)#if something happens stop for 4 seconds , let the api refresh the time counter
    print('Event created: %s' % (event.get('htmlLink')))

def insertListEvent(service,listEvents):
    addedEvents=0
    print("Time Extimated: ",round(len(listEvents)/3),"seconds")
    for event in listEvents:
        time.sleep(0.3)
        event = {
            'summary': event["Subject"],
            'start': {
                'dateTime': event["StartDateTime"],
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': event["EndDateTime"],
                'timeZone': 'Europe/Rome',
            },
        }
        insEvent = True
        while insEvent==False:
            try:
                event = service.events().insert(calendarId=calendarID, body=event).execute()
                insEvent=True
            except:
                print(datetime.datetime.now()," Error insert in calendar: ",calendarID,": Event:",event)
                insEvent= False
                time.sleep(4)#if something happens stop for 4 seconds , let the api refresh the time counter
        addedEvents+=1
        print(addedEvents,"/",len(listEvents),' - Event created: %s' % (event.get('htmlLink')))
    print("Total Events to add:",len(listEvents)," , Events added:",addedEvents)



def clearCalendar(service):
    i=0
    try:
        events_result = service.events().list(calendarId=calendarID, singleEvents=True,orderBy='startTime').execute()
    except:
        print(datetime.datetime.now()," Error getting the list!")
        return
    events = events_result.get('items', [])
    eventslength=len(events)
    if not events:
        print('No events found.')
    for event in events:
        time.sleep(0.3)
        print(i,event["id"])
        delEvent = True
        while delEvent==False:
            try:
                service.events().delete(calendarId=calendarID, eventId=event["id"]).execute()
                delEvent=True
            except:
                print(datetime.datetime.now()," Error deleting from calendar: ",calendarID,": Event:",event)
                delEvent=False
                time.sleep(4)#if something happens stop for 4 seconds , let the api refresh the time counter
        i+=1
    print("Elementi esistenti:",eventslength," , Elementi eliminati : ",i)


def clearCalendarFromToday(service):
    try:
        events_result = service.events().list(calendarId=calendarID, maxResults=99999 ,singleEvents=True,orderBy='startTime').execute()
    except:
        print(datetime.datetime.now()," Error getting the list!")
        return
    events = events_result.get('items', [])

    now= datetime.datetime.now()
    indexFrom = 0
    i=0

    for event in events:
        if( datetime.datetime.strptime(event["start"]["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S") >= now - datetime.timedelta(days=2)):
            print("TrovatoOggi")
            break
        else:
            indexFrom+=1

    eventslength=len(events)
    print("Update events from:",indexFrom ,"to",eventslength)
    print("Time Extimated: ",round((eventslength-indexFrom)/3),"seconds")

    newEvents = events[indexFrom:]
    inizio = indexFrom
    if not newEvents:
        print('No events found.')
    for event in newEvents:
        time.sleep(0.3)
        print(indexFrom,"/",eventslength,event["id"])
        delEvent = True
        while delEvent==False:
            try:
                service.events().delete(calendarId=calendarID, eventId=event["id"]).execute()
                delEvent=True
            except:
                print(datetime.datetime.now()," Error deleting from calendar:",calendarID,": Event:",event)
                delEvent=False
                time.sleep(4)#if something happens stop for 4 seconds , let the api refresh the time counter
        indexFrom+=1
        i+=1

    print("Elementi totali:",eventslength,"| Elementi da eliminare : ",len(newEvents)," , Elementi eliminati",i)
    return inizio


if __name__ == '__main__':
    getConn()
