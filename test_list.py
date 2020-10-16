from credentials import googleCalendar as myCalendar
import json
'''
struttura evento google
{'kind': 'calendar#event',
 'etag': '"3205586043328000"',
 'id': 'q4clvdtlcchd7q9jj4rfn4ndvg',
 'status': 'confirmed',
 'htmlLink': 'https://www.google.com/calendar/event?eid=cTRjbHZkdGxjY2hkN3E5amo0cmZuNG5kdmcgZmw0MW5zYzJwbGtydWpwMDd1ZGt1M29nNjBAZw',
 'created': '2020-10-15T20:17:01.000Z',
 'updated': '2020-10-15T20:17:01.664Z',
 'summary': 'ING_SFTWR',
 'creator': {'email': 'calinvasileandrei@gmail.com'},
 'organizer': {'email': 'fl41nsc2plkrujp07udku3og60@group.calendar.google.com', 'displayName': 'Eliscalendar03', 'self': True},
 'start': {'dateTime': '2020-10-05T08:45:00+02:00', 'timeZone': 'Europe/Rome'},
 'end': {'dateTime': '2020-10-05T09:46:00+02:00', 'timeZone': 'Europe/Rome'},
 'iCalUID': 'q4clvdtlcchd7q9jj4rfn4ndvg@google.com',
 'sequence': 0,
 'reminders': {'useDefault': True}}

Struttura json
{'Subject': 'InnLab', 'StartDateTime': '2021-07-20T08:45:00', 'EndDateTime': '2021-07-20T09:46:00'}
'''

'''
#get the list from google and restructure for a fast match
list_events_google = myCalendar.getEvents()
new_google_list = []
for event in list_events_google:
    new_google_list.append({"Subject":event["summary"],"StartDateTime":event["start"]["dateTime"][:-6],"EndDateTime":event["end"]["dateTime"][:-6]})

#getting the updated list events
updated_list_events = []
with open('updated_list_events.json') as json_file:
    data = json.load(json_file)
    for event in data:
        updated_list_events.append(event)

#now i have 2 list one is: updated_list_events  and the other is new_google_list


element_to_delete =[]
element_to_add = []

for event in updated_list_events:
    if event in new_google_list:
        new_google_list.remove(event)  #if i find the element i remove from the google list
        #in the google list will remain only the elements to delete
    else:
        element_to_add.append(event) #add the events which doesn't exists

element_to_delete = new_google_list #all the items which remain in the list need to be deleted



print("ELEMENT TO DELETE: [\n",element_to_delete,"\n\n]")

print("ELEMENT TO ADD: [\n",element_to_add,"\n\n]")
'''


def elementExists(event,google_list):
    for google_event in google_list:
        if(event["Subject"]==google_event["Subject"] and event["StartDateTime"]==google_event["StartDateTime"] and event["EndDateTime"]==google_event["EndDateTime"]):
            return True
    return False


list_1 = [{"Subject":"x","StartDateTime":"x","EndDateTime":"x"},{"Subject":"y","StartDateTime":"y","EndDateTime":"y"}]
list_2 = [{"Subject":"x","StartDateTime":"x","EndDateTime":"x","id":"xx"},{"Subject":"y","StartDateTime":"y","EndDateTime":"y","id":"yy"}]


print(elementExists(list_1[0],list_2))
