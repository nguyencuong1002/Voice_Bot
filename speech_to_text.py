import pyttsx3
import datetime
from time import sleep
import speech_recognition as sr
import webbrowser as wb
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

friday = pyttsx3.init()
voices = friday.getProperty('voices')

friday.setProperty('voice', voices[1].id)

driver = webdriver.Chrome(service=Service(
    'C:\\Users\\CUONG NGUYEN\\.wdm\\drivers\\chromedriver\\win32\\100.0.4896.60\\chromedriver.exe'))


def speak(audio):
    print('B.O.T: ' + audio)
    friday.say(audio)
    friday.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak(Time)
# time()


def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Chào buối sáng Khanh")
    elif hour >= 12 and hour < 18:
        speak("Chào buổi chiều Khanh")
    if hour >= 18 and hour < 24:
        speak("Chào buổi tối Khanh")
    speak("Tôi có thể giúp gì cho bạn")


def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2
        audio = c.listen(source)
    try:
        query = c.recognize_google(audio, language='vi-en')
        print("K.H.A.N.H: " + query)
    except sr.UnknownValueError:
        print("Please repeat or typing the command")
        query = str(input('Your Input Is: '))
    return query


def listen_detail_news(index):
    details_news = soup.find_all('a', {'class': 'WlydOe'})

    while True:
        listen_news = command().lower()
        if 'listen' in listen_news:
            atag = details_news[index]
            url = atag.get('href')
            driver.get(url)

            soup1 = BeautifulSoup(driver.page_source, 'html.parser')

            content_detail_news = soup1.select("article > div > p")
            if not content_detail_news:
                content_detail_news = soup1.select("article > div > div > p")
            if not content_detail_news:
                content_detail_news = soup1.select("div > p")

            for i in range(0, len(content_detail_news)):
                speak(content_detail_news[i].text)

        elif 'next' in listen_news:
            break

    # soup1 = BeautifulSoup(driver.page_source, 'html.parser')

    # content_detail_news = soup1.select("article > div > p")
    # if not content_detail_news:
    #     content_detail_news = soup1.select("article > div > div > p")
    # if not content_detail_news:
    #     content_detail_news = soup1.select("div > p")

    # for i in range(0, len(content_detail_news)):
    #     speak(content_detail_news[i].text)


if __name__ == "__main__":
    welcome()
    while True:
        query = command().lower()
        if "google" in query:
            speak("Bạn muốn tìm kiếm gì ?")
            search = command().lower()
            url = f'https://www.google.com/search?q={search}'
            driver.get(url)
            speak(
                f'Bạn đã tìm kiếm {search} trên google. Sau đây là tin tức về {search}.')

            news = driver.find_element(By.LINK_TEXT, 'Tin tức')
            news.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title_news = soup.find_all(
                'div', {'class': 'mCBkyc y355M JQe2Ld nDgy9d'})

            for i in range(0, len(title_news)):
                speak(title_news[i].text)
                sleep(1)
                listen_detail_news(i)
                sleep(2)
        elif "time" in query:
            time()
        elif 'quit' in query:
            speak("Hẹn gặp lại Khanh. Chúc bạn một ngày tốt đẹp")
            quit()
