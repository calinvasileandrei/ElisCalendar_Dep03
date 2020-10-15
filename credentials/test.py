import datetime as datetime

from credentials import googleCalendar as myCalendar
import datetime
import time


calendarID= "fl41nsc2plkrujp07udku3og60@group.calendar.google.com"

#myCalendar.printEvents(myCalendar.getConn())




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


startDateTime = datetime.datetime(2020, 10, 12, 8 ,0, 0).strftime("%Y-%m-%dT%H:%M:%S")
endDateTime = datetime.datetime(2020, 10, 12, 9 ,0, 0).strftime("%Y-%m-%dT%H:%M:%S")

myCalendar.insertEvent(myCalendar.getConn(),"TEST123",startDateTime,endDateTime)

