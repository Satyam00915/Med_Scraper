from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
import json
import time

load_dotenv()

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

gist_id = os.environ.get("GIST_ID")
gh_token = os.environ.get("GH_TOKEN")

url="https://www.truemeds.in/medicine/calcirin-forte-capsule-10-tm-cacr1-013213"

headers = {
    "user-agent": ("Mozilla/5.0 (X11; Linux x86_64)" "AppleWebKit/537.36 (KHTML, like Gecko)" "Chrome/140.0.0.0 Safari/537.36"),
    "Cookie": 'pincodeDetails={"pincode":"531021","city":"Anakapalli District","warehouseId":17,"isServiceable":true,"pincodeData":"Anakapalli District","state":"ANDHRA PRADESH"};',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

gist_url = f"https://api.github.com/gists/{gist_id}"
resp = requests.get(gist_url, headers={"Authorization": f"token {gh_token}"})
files = resp.json()["files"]
last_status = list(files.values())[0]["content"].strip()



response = requests.get(url , headers=headers)
soup = BeautifulSoup(response.text , "html.parser")
script = soup.find("script" , {"id": "__NEXT_DATA__"})
data = script.string
jsondata = json.loads(data)
availability = jsondata["props"]["pageProps"]["currentMed"]["product"]["availabilityStatus"]
if last_status == "Out of Stock" and availability != "Out of Stock":
    print("yes")
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="Your medicine Calcirin Forte is in Stock. Quick Buy",
        to='whatsapp:+919866824490'
    )
    print(availability)
else:   
    print("Still out of stock")
    
update_data = {
    "files": {
        list(files.keys())[0]: {"content": "Out of Stock"}
    }
}
requests.patch(gist_url, headers={"Authorization": f"token {gh_token}"}, json=update_data)




