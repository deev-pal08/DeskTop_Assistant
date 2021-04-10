import pyttsx3
import datetime
import time
import winsound
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import sys
import pafy
import vlc
import math
import requests
import pywhatkit
from googletrans import Translator
from bs4 import BeautifulSoup
try:
    from googlesearch import search
except ImportError:
    print("No such module Found")
    speak("No such module found")

engine = pyttsx3.init('sapi5')  #sapi5 in a microsoft api for enabling voice commands
voices = engine.getProperty('voices') #for getting the property of voices which is an array consisting
# of all the voices of our windows
# print(voices[1].id) voices[1] = girl and voices[0] = boy
engine.setProperty('voice', voices[1].id) # enabling voice command for voice id 0(can also b 1);


def speak(audio):
    #speak function for novo to speak out voices given as input
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    #function to take command from user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Regognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query} \n")
    except Exception as e:
        print(e)
        print("Can U Say That Again...") 
        # speak("Can U Say That Again...")
        return "None"
    return query

def wishMe():
    #first fuction to be called for greeting the user
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Deev")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Deev")
    else:
        speak("Good Evening Deev")

# def knowName():
#     speak("Can i Please know your name")
#     return takeCommand()

def reminders(query):
    if 'set reminder' in query:
        speak("which date and time should i set a remimder")
        date = takeCommand()
        speak("What should i set reminder for")
        remind = takeCommand()
        f = open("Reminders.txt","a")
        f.write(f"You have a reminder on {date} for {remind}\n")
        f.close()
        speak(f"Reminder set for {remind} on {date}")

    elif 'give reminders' in query:
        f = os.path.getsize("Reminders.txt")
        if f == 0:
            speak(f"Sorry {name} you do not have any reminder, Thank You")
        else:
            read = open("Reminders.txt","r")
            for x in read:
                print(x)
                speak(x)
            read.close()
        
    elif 'remove all reminders' in query:
        speak("Are you sure you want to delete all reminders")
        ans = takeCommand().lower()
        if 'yes' in ans:
            f = open("Reminders.txt","r+")
            f.seek(0)
            f.truncate()
            speak("All reminders deleted successfull")
            f.close()
        else:
            speak("Operation Cancelled")

def sendEmail(to, content):
    try : 
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('Your.Email@gmail.com','Password')
        server.sendmail('Your.Email@gmail.com',to,content)
        server.close()
    except Exception as e:
        print(e)
        print("Sorry Error in sending mail....Please try again")
        speak("Sorry Error in sending mail....Please try again")

def callFunc():
    hello = takeCommand().lower()
    if 'hello novo' in hello:
        return 'yes'
    return 'no'

def openThings(query):
    if 'youtube' in query:
        print("Opening Youtube...\n")
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com/")
    elif 'code' in query:
        print("Opening VS Code...\n")
        speak("Opening VS Code")
        codePath = "C:\\Users\\ADMIN\\Desktop\\STUDY MATERIALS\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)
    elif 'questions' in query:
        print("Opening Questions...\n")
        speak("Opening Questions")
        codePath = "C:\\Users\\ADMIN\\Desktop\\STUDY MATERIALS\\CODING QUESTIONS\\Most Important"
        os.startfile(codePath)
        
    elif 'chrome' in query:
        print("Opening Google Chrome...\n")
        speak("Opening Google Chrome")
        codePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(codePath)

    elif 'whatsapp' in query:
        print("Opening whatsapp...\n")
        speak("opening whatsapp")
        webbrowser.open("https://web.whatsapp.com/")

def timeAndDate(query):
    if 'time' in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{name}, the time is : {time}")
        speak(f"{name}, the time is : {time}")
    elif 'date' in query:
        date = datetime.datetime.now().strftime("%A:%d:%B:%Y")
        print(f"{name}, the date is : {date}")
        speak(f"{name}, the date is : {date}")

def convertor(query,res):
    query = query.replace("novo","")
    query = "Calculateme.com" + query
    url = ""
    for j in search(query,tld='co.in',num=1,stop=1,pause=1):
        url = j
        break
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ans = soup.find(class_="answer-box text-xl")
    con = ans.find(class_="font-weight-bold")
    print(con.get_text())
    speak(con.get_text())

def mathsProblems(query):
    res = [float(i) for i in query.split() if i.isdigit()]
    query = query.lower()
    if 'x' in query:
        print(res[0] * res[1])
        ans = str(res[0] * res[1])
        speak(ans)
    elif 'divided' in query or '/' in query:
        if res[1] == 0:
            print("Undefined")
            speak("Undefined")
        else:
            print(res[0] / res[1])
            ans = str(res[0] / res[1])
            speak(ans)
    elif 'plus' in query or '+' in query:
        print(res[0] + res[1])
        ans = str(res[0] + res[1])
        speak(ans)
    elif '-' in query or 'minus' in query:
        print(res[0] - res[1])
        ans = str(res[0] - res[1])
        speak(ans)
    elif 'power' in query:
        print(res[0] ** res[1])
        ans = str(res[0] ** res[1])
        speak(ans)
    elif 'mod' in query:
        print(res[0] % res[1])
        ans = str(res[0] % res[1])
        speak(ans)
    elif 'square' in query:
        print(math.sqrt(res[0]))
        ans = str(math.sqrt(res[0]))
        speak(ans)
    elif 'factorial' in query:
        print(math.factorial(int(res[0])))
        ans = str(math.factorial(int(res[0])))
        speak(ans)
    elif 'gcd' in query:
        print(math.gcd(int(res[0]),int(res[1])))
        ans = str(math.gcd(int(res[0]),int(res[1])))
        speak(ans)
    elif 'log base 10' in query or 'log10' in query:
        n = len(res)
        print(math.log10(res[n-1]))
        ans = str(math.log10(res[n-1]))
        speak(ans)
    elif 'log base 2' in query or 'log2' in query:
        n = len(res)
        print(math.log2(res[n-1]))
        ans = str(math.log2(res[n-1]))
        speak(ans)
    else:
        try:
            convertor(query,res)
        except Exception:
            speak("Sorry for the inconvenience, cannot perform the operation right now")

def speakToMenovo(query):
    if 'who are you novo' in query:
        speak(f"My name is novo, i am your desktop assistant, how can i help you {name}")
    elif 'goodbye' in query:
        speak("Are you sure you want to quit")
        ans = takeCommand().lower()
        if 'yes' in ans or 'yah' in ans or 'yeah' in query:
            speak(f"GoodBye {name} it was nice meeting you")
            sys.exit(f"GoodBye {name} it was nice meeting you")
        else:
            speak("Operation Cancelled")
    elif 'please say' in query:
        query = query.replace("novo please say","")
        speak(query)
    elif 'thank you' in query:
        speak("It was nice helping you Deev,what else can i do for u")
    elif 'how are you novo' in query or 'how u doing novo' in query:
        speak("I m fine deev,How are you?")
        reply = takeCommand().lower()
        if 'no' in reply or 'not' in reply:
            speak("That's a very bad news, how may i help u?")
        else:
            speak("good to head from u,How may i help u?")
    elif 'sleep' in query:
        speak("i sleep when u terminate this python code,orelse i m very active all day long")
    elif 'who am i' in query:
        speak("Your name is deev, you are the one who created me, how can i help u")
    


def playSongsForMe(query):
    song = query.replace("play","") 
    url = ""
    for j in search(song,tld="co.in",num=1,stop=1,pause=2):
        url = j
        break
    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.play()
    speak(f"playing {song}")
    try : 
        while(True):
            command = takeCommand().lower()
            if 'pause' in command:
                media.set_pause(1)
                speak("song paused")
            elif 'resume' in command or 'play' in command:
                media.play()
                speak("song resumed")
            elif 'stop' in command:
                media.stop()
                speak("song stopped")
                break
    except Exception:
        print("Song Stopped")

def searchOnlinenovo(query):
    if 'wikipedia' in query:
        try :
            speak("What do you want me to search")
            find = takeCommand()
            speak("Searching Wikipedia...")
            results = wikipedia.summary(find, sentences=2)
            speak("According To Wikipedia")
            print(results)
            speak(results)
        except Exception:
            speak(f"Sorry No Such page as {find} found in wikipedia")

    elif 'google' in query:
        speak("what do u want me to search")
        find = takeCommand().lower()
        find = find.replace("search","")
        speak(f"Searching google for : {find}")
        for j in search(find,tld="co.in",num=5,stop=5,pause=2):
            webbrowser.open(j)
    elif "search" in query:
        query = query.replace("novo","")
        speak("Searching google")
        for j in search(query,tld="co.in",num=5,stop=5,pause=2):
            webbrowser.open(j)
        

def alarmControls(query):
    res = query.split()
    time = ""
    extra = []
    for i in res:
        if ':' in i or i.isdigit():
            if time == "":
                time = i
            extra.append(i)
    if ':' not in time:
        time = time[0] + ":" + time[1] + time[2]
        time = "0" + time
    else:
        if len(time) == 4:
            time = "0" + time
    if 'p.m.' in query:
        n = int(time[0:2])
        n += 12
        time = str(n) + time[2:5]
    if len(extra) > 1:
        t2 = extra[1]
        num = ""
        if len(t2) == 4:
            num = "0" + str(t2[0])
        else:
            num = str(t2[0:2])
        time = time[0:3] + num
    print(time)
    f = open("TimeAlarm.txt","a")
    f.write(time)
    f.close()
    speak(f"alarm set for {time}")

def getNewsHeadlines():
    url = "https://www.ndtv.com/top-stories"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_news = soup.find(class_="new_storylising")
    news = get_news.find_all(class_="nstory_header")
    speak("The headLines Are As Follows:")
    num = 0
    for i in news:
        print(f"{num} : {i.get_text()}")
        speak(i.get_text())
        time.sleep(1)
        num+=1

def getTemperature(query):
    res = query.split()
    city = res[len(res) - 1]
    for j in search(f"bbc {city} weather forcast",tld="co.in",num=1,stop=1,pause=1):
        url = j
        break
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="daylink-0")
    forecast_items = seven_day.find_all(class_="wr-day-temperature__high")
    print(f"The Weather Forecast for {city} is as follows:\n")
    speak(f"The Weather Forecast for {city} is as follows:")
    if len(forecast_items) != 0:
        tonight = forecast_items[0]
        upperC = tonight.find(class_="wr-value--temperature--c").get_text()
        upperF = tonight.find(class_="wr-value--temperature--f").get_text()
        print(f"On a higher scale the temperature can rise up to:{upperC}C or {upperF}F")
        speak(f"On a higher scale the temperature can rise up to:{upperC}Celcius or {upperF}Farenheit")

    forecast_items = seven_day.find_all(class_="wr-day-temperature__low")
    tonight = forecast_items[0]
    lowerC = tonight.find(class_="wr-value--temperature--c").get_text()
    lowerF = tonight.find(class_="wr-value--temperature--f").get_text()

    sun = soup.find_all(class_="wr-c-astro-data__time")
    sunrise = sun[0].get_text()
    sunset = sun[1].get_text()

    extras = soup.find_all(class_="wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--")
    humidity = extras[0].get_text()
    pressure = extras[2].get_text()

    forecast_items = seven_day.find_all(class_="wr-day__details")
    tonight = forecast_items[0]
    condition = tonight.find(class_="wr-day__details__weather-type-description").get_text()

    print(f"On a lower scale the temperature can fall up to:{lowerC}C or {lowerF}F")
    speak(f"On a lower scale the temperature can fall up to:{lowerC}Celcius or {lowerF}Farenheit")

    print(f"Conditions can be : {condition}")
    speak(f"Conditions can be : {condition}")

    print(f"{humidity}")
    speak(f"{humidity}")

    print(f"{pressure}")
    speak(f"{pressure}")

    print(f"sunrise : {sunrise} a.m.")
    speak(f"sunrise : {sunrise} a.m.")

    print(f"sunset : {sunset} p.m.")
    speak(f"sunset : {sunset} p.m.")

def sendWhatsappMessage(query):
    res = query.split()
    n = len(res)
    name = res[n-1]
    read = open("Numbers.txt","r")
    number = []
    for x in read:
        if name in x:
            number = x.split()
            break
    read.close()
    if len(number) == 0:
        speak(f"Sorry no name with {name} found")
    else:
        speak("what do you want to send?")
        msg = takeCommand()
        print("Sending Message....")
        speak("Sending Message....")
        currTimeHr = datetime.datetime.now().strftime("%H")
        currTimeMin = datetime.datetime.now().strftime("%M")
        hrs = int(currTimeHr)
        minutes = int(currTimeMin) + 2
        pywhatkit.sendwhatmsg(number[1],msg,hrs,minutes)
        speak("Message Sent Successfully")

def getTranslatedVoice():
    translator = Translator()
    result = translator.translate("hello there",dest='bn')
    print(result.text)

def remindMenovo():
    fs = os.path.getsize("Reminders.txt")
    if fs != 0:
        speak(f"You Have a few Reminders {name},Do you want me to tell them")
        ans = takeCommand().lower()
        if 'yes' in ans:
            read = open("Reminders.txt","r")
            for x in read:
                print(x)
                speak(x) 
            read.close()      
        else:
            speak("Okay Thank You Deev")

def alarmClockReminders():
    fa = os.path.getsize("TimeAlarm.txt")
    if fa != 0: 
        music_dir = "C:\\Users\\ADMIN\\Desktop\\STUDY MATERIALS\\jarvis\\alarmMusic"
        alarm = os.listdir(music_dir)
        current = datetime.datetime.now().strftime("%H:%M")
        allTime = open("TimeAlarm.txt","r")
        for x in allTime:
            if x == current:
                os.startfile(os.path.join(music_dir, alarm[0]))
        allTime.close()

if __name__ == "__main__":
    hello = callFunc()
    while 'yes' not in hello:
        hello = callFunc()
    wishMe()
    name = "Deev"
    remindMenovo()
    speak("This is novo, Please tell me how may i help you") 
    while True:
        alarmClockReminders()

        query = takeCommand().lower()

        if 'search' in query:
            try:
                searchOnlinenovo(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
                
        elif 'open' in query:
            try :
                openThings(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'time' in query or 'date' in query:
            try:
                timeAndDate(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'send email' in query:
            speak("Sir, please specify the email adddress")
            emailAddress = takeCommand().lower()
            speak("What should i say, Sir")
            content = takeCommand()
            sendEmail(emailAddress,content)
            print(f"Sending email to : {emailAddress}\n")
            speak(f"Sending email to : {emailAddress}")
        
        elif 'song' in query or 'songs' in query :
            try:
                playSongsForMe(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'temperature' in query or 'weather' in query:
            try:
                getTemperature(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'set reminders' in query or 'give reminders' in query or 'remove all reminders' in query:
            try:
                reminders(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")

        elif 'news' in query:
            try:
                getNewsHeadlines()
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'translate' in query:
            # try:
                getTranslatedVoice()
            # except Exception:
                # speak("Sorry for the inconvenience, cannot perform the operation right now")

        elif 'shutDown' in query:
            speak("Are you sure you want to shut down")
            ans = takeCommand().lower()
            if 'yes' in ans:
                speak("Shutting down computer")
                os.system("shutdow /s /t 30")
            else:
                speak("Opeartion Cancelled")

        elif 'how much' in query or 'what is' in query:
            try:
                mathsProblems(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'send message' in query:
            try:
                sendWhatsappMessage(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'set an alarm' in query:
            try:
                alarmControls(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        
        elif 'novo' in query:
            try:
                speakToMenovo(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
        elif 'search' in query:
            try:
                searchOnlinenovo(query)
            except Exception:
                speak("Sorry for the inconvenience, cannot perform the operation right now")
             