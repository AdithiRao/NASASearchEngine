from flask import Flask, render_template, request
from pip._vendor import requests
import urllib.request, json
from datetime import date

app = Flask(__name__)

#Loads when the file is first loaded
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def getvalue():
    #Initializes all the variables tused later
    location = ""
    home = ""
    dateFilter = ""
    past=""
    pastSearches = []
    dateOut = ""
    lOut = ""
    #tries to get information from fields on the html pages
    try:
        search = request.form['Search']
        qOut = search
    except:
        pass
    try:
        home = request.form['Home']
    except:
        pass
    try:
        location = request.form['location']
        lOut = "Location: " + location + "  "
    except:
        pass
    try:
        dateFilter = request.form['datefilter']
        dateOut = "Date Range: " + dateFilter
    except:
        pass

    payload = {'q': search, "media_type":"image"}

    #If the user wants to go back to the index.html page
    if home != "":
        return render_template('index.html')

    #Adds to the payload as needed
    if location!="":
        payload['location'] = location
    if dateFilter != "":
        payload['year_start'] = dateFilter[6:10]
        payload['year_end'] = dateFilter[19:23]

    #Used to output search queries back to the user
    if lOut == "" and dateOut != "":
        dateOut = "Filtered by: " + dateOut
    elif lOut != "":
        lOut = "Filtered by: " + lOut


    r = requests.post("https://images-api.nasa.gov/search", params=payload)
    image_urls = []
    descr = []
    centers = []
    date_cr = []
    nasa_id = []
    photographers = []
    locations = []
    #Loads the JSON file
    with urllib.request.urlopen(r.url) as url:
        data = json.loads(url.read().decode())


    leng = len(data["collection"]["items"])
    for i in range(leng):
        #If we need to filter by date
        if dateFilter != "":
            specYear = int(data["collection"]["items"][i]['data'][0]['date_created'][0:4])
            specMonth = int(data["collection"]["items"][i]['data'][0]['date_created'][5:7])
            specDay = int(data["collection"]["items"][i]['data'][0]['date_created'][8:10])
            year1 = int(dateFilter[6:10])
            month1 = int(dateFilter[0:2])
            day1 = int(dateFilter[3:5])
            year2 = int(dateFilter[19:23])
            month2 = int(dateFilter[13:15])
            day2 = int(dateFilter[16:18])
            #Makes sure the entry date is in between the passed in dates
            if(date(year1,month1,day1) < date(specYear,specMonth, specDay) and
             date(specYear,specMonth, specDay) <date(year2,month2,day2)):
                image_urls.append(data["collection"]["items"][i]['links'][0]['href'])
                descr.append(data["collection"]["items"][i]['data'][0]['title'])
                centers.append(data["collection"]["items"][i]['data'][0]['center'])
                date_cr.append(data["collection"]["items"][i]['data'][0]['date_created'][0:10])
                try:
                    locations.append(data["collection"]["items"][i]['data'][0]['location'])
                except KeyError:
                    locations.append("N/A")
        #if no date filter is specified
        else:
            image_urls.append(data["collection"]["items"][i]['links'][0]['href'])
            descr.append(data["collection"]["items"][i]['data'][0]['title'])
            centers.append(data["collection"]["items"][i]['data'][0]['center'])
            date_cr.append(data["collection"]["items"][i]['data'][0]['date_created'][0:10])
            try:
                locations.append(data["collection"]["items"][i]['data'][0]['location'])
            except KeyError:
                locations.append("N/A")


    length = len(image_urls)
    #returns all the variables needed for the parse.html file to work
    return render_template('parse.html', qOut=qOut, lOut=lOut, dateOut=dateOut, images=image_urls, length=length,
     descr= descr, centers=centers, date = date_cr, locat = locations, past = pastSearches)
