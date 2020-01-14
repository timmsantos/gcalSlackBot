import datetime
import json
import requests
import os
from datetime import date
from cal_setup import get_calendar_service
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)

from pathlib import Path 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

def main():
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List of 10 events')
   events_result = service.events().list(
       calendarId='primary', timeMin=now,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       slackMessage ('No Events Found')
   for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        slackMessage(start + "   " + event['summary'])



def slackMessage (passedMessage):
    slack_msg = {"text":passedMessage, "username":"TimBothy", "icon_emoji":":man-shrugging:"}
    requests.post(slack_webhook, data=json.dumps(slack_msg))

if __name__ == '__main__':
   main()