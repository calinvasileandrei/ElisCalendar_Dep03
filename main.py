import xlrd
import xlwt
import datetime
import time
import requests
import ssl
from credentials import googleCalendar as myCalendar
import json

#WebSSL certificates
ssl._create_default_https_context = ssl._create_unverified_context
#download the xlsx file from the link
link = "https://cedelcloud-my.sharepoint.com/:x:/g/personal/g_tomeno_elis_org/EdfyxBa5gSFNivc2-aj7G0IB48bm609wlXrkbQc7ITLoww?download=1"

#Defining vars
listEventi = []
#insert the time range
Orario = ["8,45-9,45", "9,45-10,45", "10,45-11,45", "11,45-12,45", "14,15-15,15", "15,15-16,15", "16,15-17,15","17,15-18,15"]


def getList():
    print("Getting the list")
    #Downloading the file
    webFile = requests.get(link)

    #Open Workbook
    wb = xlrd.open_workbook(file_contents=webFile.content)

    #check the sheet index I want
    namesSheets = wb.sheet_names()
    sheetIndex=0
    for name in namesSheets:
        if(name == "2 anno AA 20-21" ):
            break
        else:
            sheetIndex+=1

    print("Sheet 2 anno AA 20-21 index:",sheetIndex)

    #select the index of the sheet
    sheet = wb.sheet_by_index(sheetIndex)

    # the first month of the calendar, 10 = october
    startMonth = 10
    # select the year
    startYear = 2020

    #the number of the month in the exel file
    monthNumber = 10
    hourNumber = 7

    for z in range(0, monthNumber): #for each month = z
        currentColumnMonth = z * 10
        if (startMonth == 13): #startMonth is a int and when it goes over 12 i need to reset the year
            startMonth = 1
            startYear += 1

        for i in range(sheet.nrows): # i= row
            if (i != 0 and i<35): # i need to skip the first blank row and 
                if (sheet.cell_value(i, currentColumnMonth) != ""): #check the value if it is not null
                    dataNum = int(sheet.cell_value(i, currentColumnMonth))
                    completeData = [int(startYear),int(startMonth),int(dataNum)]

                    # cycle foreach hour
                    j = 2 #increment number for getting the right column
                    for n in range(0, hourNumber): # number of hours of lessons
                        subject = sheet.cell_value(i, j + currentColumnMonth) # get the subject
                        Time = (sheet.cell_value(1, j + currentColumnMonth)).split("-") #get the time splitted
                        #splitting the unic time in start and end time
                        startTime = Time[0].split(",")
                        endTime =Time[1].split(",")

                        #creating the datetime string formatted
                        startDateTime = datetime.datetime(int(completeData[0]),int(completeData[1]),int(completeData[2]),int(startTime[0]),int(startTime[1]),0).strftime("%Y-%m-%dT%H:%M:%S")
                        endDateTime = datetime.datetime(int(completeData[0]),int(completeData[1]),int(completeData[2]),int(endTime[0]),int(endTime[1])+1,0).strftime("%Y-%m-%dT%H:%M:%S")

                        if (subject and subject!="x"): # i there is a subject i add the event
                            listEventi.append({"Subject":subject, "StartDateTime":startDateTime,"EndDateTime":endDateTime})
                        j += 1 # i move a column further for getting the next hour
        startMonth += 1 # increment the int month counter

def elementExists(event,google_list):
    for google_event in google_list:
        if(event["Subject"]==google_event["Subject"] and event["StartDateTime"]==google_event["StartDateTime"] and event["EndDateTime"]==google_event["EndDateTime"]):
            return True
    return False

def removeElementGoogleList(event_to_remove,new_google_list):
    for event_google in new_google_list:
        if(event_to_remove["Subject"]==event_google["Subject"] and event_to_remove["StartDateTime"]==event_google["StartDateTime"] and event_to_remove["EndDateTime"]==event_google["EndDateTime"]):
            new_google_list.remove(event_google)

    return new_google_list

def updateList(updated_list_events):
    # get the list from google and restructure for a fast match
    list_events_google = myCalendar.getEvents()
    new_google_list = []
    for event in list_events_google:
        new_google_list.append({"Subject": event["summary"], "StartDateTime": event["start"]["dateTime"][:-6],
                                "EndDateTime": event["end"]["dateTime"][:-6],"id":event["id"]})
    # now i have 2 list one is: updated_list_events  and the other is new_google_list

    element_to_add = []

    for event in updated_list_events:
        if elementExists(event,new_google_list):
            removeElementGoogleList(event,new_google_list) # if i find the element i remove from the google list
            # in the google list will remain only the elements to delete
        else:
            element_to_add.append(event)  # add the events which doesn't exists

    element_to_delete = new_google_list  # all the items which remain in the list need to be deleteid

    print("ELEMENT TO DELETE: [\n", element_to_delete, "\n\n]")
    if(len(element_to_delete)>0):
        myCalendar.clearCalendarFromList(element_to_delete)
    else:
        print("List is up-to date, no event need to be deleted")

    print("ELEMENT TO ADD: [\n", element_to_add, "\n\n]")
    if(len(element_to_add) >0):
        myCalendar.insertListEvent(element_to_add)
    else:
        print("List is up-to date, no element need to be added")


def googleOps(): #google calendar operations
    getList()
    updateList(listEventi)
    #should i check if the new update has the same event list of the last one
    #If true skip the update
    #IF not update
    #print("Elementi Totali : ",len(listEventi))
    #myCalendar.clearCalendar(myCalendar.getConn())
    #indexFrom = myCalendar.clearCalendarFromToday(myCalendar.getConn()) #clear all the events
    #myCalendar.insertListEvent(listEventi[indexFrom:]) #add all the events


if __name__ == '__main__':
     #I should add a check if all events already exists
     #IF not i should add all of them
     #IF exists I should update only the newest
     #while True:



     print("Elis calendar Update: ",datetime.datetime.now())
     googleOps()
     print("Elis calendar Finish Update: ",datetime.datetime.now())
        #time.sleep(86400) #every day repeat

  

