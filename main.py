import xlrd
import xlwt
import datetime
import time
import requests
import ssl
from credentials import googleCalendar as myCalendar

#WebSSL certificates
ssl._create_default_https_context = ssl._create_unverified_context
#download the xlsx file from the link
link = "https://cedelcloud-my.sharepoint.com/:x:/g/personal/i_colosimo_elis_org/EUvKVPC9g_5Ni2LKpC54IgoBFQzO1E6dU2IB8wnSIjU9fw?download=1"

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
        if(name == "1 annoLeone" ):
            break
        else:
            sheetIndex+=1

    print("Sheet 1 annoLeone index:",sheetIndex)

    #select the index of the sheet
    sheet = wb.sheet_by_index(sheetIndex)

    # the first month of the calendar, 10 = october
    startMonth = 10
    # select the year
    startYear = 2019

    #the number of the month in the exel file
    monthNumber = 10
    hourNumber = 8

    for z in range(0, monthNumber): #for each month = z
        currentColumnMonth = z * 11
        if (startMonth == 13): #startMonth is a int and when it goes over 12 i need to reset the year
            startMonth = 1
            startYear += 1

        for i in range(sheet.nrows): # i= row
            if (i != 0): # i need to skip the first blank row
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

                        if (subject): # i there is a subject i add the event
                            listEventi.append({"Subject":subject, "StartDateTime":startDateTime,"EndDateTime":endDateTime})
                        j += 1 # i move a column further for getting the next hour
        startMonth += 1 # increment the int month counter


def googleOps(): #google calendar operations
    getList()
    #should i check if the new update has the same event list of the last one
    #If true skip the update
    #IF not update
    print("Elementi Totali : ",len(listEventi))
    indexFrom = myCalendar.clearCalendarFromToday(myCalendar.getConn()) #clear all the events
    myCalendar.insertListEvent(myCalendar.getConn(), listEventi[indexFrom:]) #add all the events


if __name__ == '__main__':
     #I should add a check if all events already exists
     #IF not i should add all of them
     #IF exists I should update only the newest
     while True:
        print("Elis calendar Update: ",datetime.datetime.now())
        googleOps()
        print("Elis calendar Finish Update: ",datetime.datetime.now())
        time.sleep(86400) #every day repeat
  

