import requests
from smtplib import SMTP
import os 

API_KEY = os.environ.get("OWM_API_KEY")   
MY_LAT = os.environ.get("MY_LAT")
MY_LONG = os.environ.get("MY_LON")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "cnt": 7,
    "appid": API_KEY
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

weather_data = response.json()["list"]

will_rain = False
for time_stomp in weather_data:
    for weather in time_stomp["weather"]:
        if weather["id"] < 700:
            will_rain = True

if will_rain:
    MY_EMAIL = os.environ.get("MY_EMAIL")
    APP_PASS = os.environ.get("MY_PASS")
    RECEIVER = os.environ.get("RECEIVER")

    with SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()

        connection.login(user=MY_EMAIL, password=APP_PASS)

        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECEIVER, msg="Subject: Weather Notification \n\n There's a probability of raining today. Don't forget to bring an umbrella!".encode('utf-8'))

        print("Notification sent!")
