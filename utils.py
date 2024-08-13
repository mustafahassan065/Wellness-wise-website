# utils.py
import jwt
import requests
import json
import datetime
from django.conf import settings

def generate_zoom_meeting():
    headers = {
        'alg': 'HS256',
        'typ': 'JWT',
    }

    payload = {
        'iss': settings.ZOOM_API_KEY,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
    }

    token = jwt.encode(payload, settings.ZOOM_API_SECRET, algorithm='HS256')

    meetingdetails = {
        "topic": "Meeting with Wellness Expert",
        "type": 2,
        "start_time": "2020-03-31T12:02:00Z",
        "duration": "45",
        "timezone": "Europe/Madrid",
        "agenda": "test",

        "recurrence": {"type": 1,
                       "repeat_interval": 1
                       },
        "settings": {"host_video": "true",
                     "participant_video": "true",
                     "join_before_host": "False",
                     "mute_upon_entry": "False",
                     "watermark": "true",
                     "use_pmi": "False",
                     "approval_type": 2,
                     "audio": "voip",
                     "auto_recording": "none"
                     }
    }

    response = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers={
            'authorization': f'Bearer {token}',
            'content-type': 'application/json'
        },
        data=json.dumps(meetingdetails),
    )

    meeting_info = response.json()
    return meeting_info['join_url']
