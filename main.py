#Rune
import webbrowser
import urllib.request
import datetime
import pytz
import random

""" Returns the current period number or 0 if it is not during school hours"""

def get_period_number(hour, minute):

  if (hour < 8 or hour >= 15):
    return 0
  elif (hour == 9 and (minute >= 44 and minute < 49)):
    return -3
  elif (hour == 8 and (minute >= 0 and minute < 47)):
    return 1
  elif (hour == 8 and minute >= 52 or (hour == 9 and minute < 39)):
    return 2
  elif (hour == 9 and minute >= 54 or (hour == 10 and minute < 41)):
    return 3
  elif (hour == 10 and minute >= 46 or (hour == 11 and minute < 33)):
    return 4
  elif (hour == 11 and minute >= 38 or (hour == 12 and minute < 24)):
    return -2
  elif (hour == 12 and minute >= 26 or (hour == 13 and minute < 16)):
    return 5
  elif (hour == 13 and minute >= 21 or (hour == 14 and minute < 8)):
    return 6
  elif (hour == 14 and minute >= 13):
    return 7
  else:
    return -1
  

# add code below to set cur_day equal to the name of the current day when this script is run (e.g. "Tuesday")
# and to set cur_period equal to the number of the current period when this script is run (e.g. 3)
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday","Sunday"]
cur_day = weekdays[datetime.date.today().weekday()]
cur_hour = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%H')
cur_minute = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%M')
cur_period = get_period_number(int(cur_hour), int(cur_minute))

# FOR TESTING ONLY
#cur_day = "Monday"
#cur_period = 7
# ABOVE FOR TESTING ONLY-- comment above 2 lines out before submitting your project, but do NOT delete them, as
# I will uncomment them and use them to test your script works with various days/periods.

# In the above sample Google Sheets URL, everything between the /d/ and /edit? is the unique spreadsheet ID.
print("In the following line, please enter a Google Spreadsheet ID. The ID will be between /d/ and /edit?")
unique_spreadsheet_id = input("Input Spreadsheet ID: ")

unique_spreadsheet_id = "1nUhzyJdohkQg7gMCkwN_O05mF6EDDSH9-EZAk73j6NE"
# replace the above with the unique ID of the Google Sheet you want to access

url = "https://docs.google.com/spreadsheets/d/" + unique_spreadsheet_id + "/gviz/tq?tqx=out:csv&sheet="+cur_day
webpageObject = urllib.request.urlopen(url)
# webpageObject is an object of class HTTPResponse

# we need to decode what we have in this HTTPResponse object
# to do that, we can use the read() method of the HTTPResponse class.
webpage = webpageObject.read().decode('utf-8')
data_array = []
index = 0

for i in webpage.splitlines():
    i = i.split(",")
    data_array.append(i)

currently_avaliable = []

for element in data_array:
    if (int(element[1][1:2]) == cur_period):
        currently_avaliable.append(element[0])

currently_avaliable.sort()

file = open("frees.html", "w")

file.write(""" <!Doctype HTML>
<html lang="en">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,600&display=swap" rel="stylesheet">
<title> Who is free? </title>
<style>""")
index = 1
for person in currently_avaliable:
    file.write("#person-"+ str(index)+" { transform: rotate(" + str(int(random.random() * 181)) + "deg); }\n")
    index += 1
file.write("""
#listbody { align-items: center; }
#clock { text-align: center; color: #464555; font-family: "DM Sans", sans-serif; font-size: 70px; padding: 0; margin: 0;}
h2 { text-align: center; color: #464555; font-family: "DM Sans", sans-serif; font-size: 30px;}
ul {text-align: left; font-size: 20px; list-style: none; padding-inline-start: 0px; animation: marquee-vertical 13s linear infinite;}
li {text-align: left; margin: 7px; color: #464555; font-family: "DM Sans", sans-serif; font-size: 20px;}
#image-div {text-align: center;}
#image-div:hover {animation: smooth-zoom;}
img {width: 55%; margin-top: 5%; margin-bottom: -5%;}
@keyframes smooth-zoom {from {transform: scale(0);} to {transform: scale(1.1);}}
@keyframes marquee-vertical {from {transform: translateY(0%);} to {transform: translateY(500%);}}
</style>

<script>
function showTime()
{
    const date = new Date();
    let hours = String(date.getHours());
    if (hours.length == 1) {
        hours = "0" + hours
    }
    let minutes = String(date.getMinutes());
    if (minutes.length == 1) {
        minutes = "0" + minutes
    }
    time = hours + ":" + minutes
    document.getElementById("clock").innerHTML = time;
    setTimeout("showTime()",1000);
}

</script>

</head>
<body onLoad="showTime()">
<div id="image-div">
    <img alt="title" src=\"./web_name.png\">
</div>
<div> 

""")

file.write("""<div id="clock"> </div>\n</div>\n""")
#datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%H')
#cur_minute = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%M')

header_prompt = ""

if (len(currently_avaliable) == 0):
    if(cur_period == -1):
        header_prompt = "GET TO CLASS!!"
    elif(cur_period == -2):
        header_prompt = "It's lunchtime, everyone is available!"
    elif(cur_period == -3):
        header_prompt = "It's homeroom, go there now!"
    elif(cur_period == 0):
        header_prompt = "School is not in session at the moment"
    else:
        header_prompt = "No one is currently available"
else:
    if(len(currently_avaliable) > 1):
        people = "people"
    else:
        people = "person"
    header_prompt = "It is currently " +cur_day + ", period " + str(cur_period) +"<br>" + "There are currently " + str(len(currently_avaliable)) + " " + people + " available"

file.write("<div>\n \t<h2>" + header_prompt + "</h2>\n</div>\n")
if (len(currently_avaliable) != 0):
    file.write("<div id=\"listbody\">\n<ul>\n")
    index = 1
for person in currently_avaliable:
    file.write("<li id=\"person-" + str(index) + "\">"+person[1:len(person)-1]+"</li>\n")
    index += 1
if (len(currently_avaliable) != 0):
    file.write("</ul>\n</div>\n")
file.write("""</body>
""")

file.close()
