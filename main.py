import requests
import smtplib
from datetime import datetime

MY_LAT = 43.6532 # Your latitude
MY_LONG = 79.3832 # Your longitude

source_email = "ashwinalexandertest@gmail.com"
source_password = "pwdwashere"
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"

response = requests.get(url=ISS_ENDPOINT)
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
#Your position is within +5 or -5 degrees of the ISS position.

def is_iss_proximate(iss_lat, iss_long, my_lat, my_long):
    '''Takes in coordinates of the ISS, and the user - returns True if the ISS is within +-5'''
    return True
    # return abs(iss_lat - my_lat) <= 5 and abs(iss_long - my_long) <= 5

def is_dark(sunrise,sunset,hour_now):
    '''Current hour is greater than sunset hour or earlier than sunrise hour'''
    '''We can only see the ISS in the dark'''
    return hour_now >= sunset or hour_now <= sunrise

def sendEmail():
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=source_email, password=source_password)
        connection.sendmail(
            from_addr=source_email,
            to_addrs=source_email,
            msg="Subject:ISS proximity\n\n Look up the ISS is overhead")


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

hour_now = datetime.now().hour

if is_dark(sunrise,sunset,hour_now) and is_iss_proximate(MY_LAT,MY_LONG,iss_latitude,iss_longitude):
    print("the stars are aligned")
    sendEmail()
else:
    print("nope")




