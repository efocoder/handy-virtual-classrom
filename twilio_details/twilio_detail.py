from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client, video
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


import os
from django.contrib.sites.shortcuts import get_current_site

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
api_sid = os.getenv('API_SID')
api_secret = os.getenv('API_SECRET')

client = Client(account_sid, auth_token)

# client.connect_apps()

def create_room(request, unique_name):
    current_site = get_current_site(request)
    url = current_site.domain

    try:
        room = client.video.rooms.create(
            record_participants_on_connect=True,
            status_callback=url,
            type='group',
            unique_name=unique_name
        )
        print(room)
        return room
    except TwilioRestException as e:
        print(e)


def generate_access_token(user_id, room):
    # Create an Access Token
    token = AccessToken(account_sid, api_sid, api_secret)

    # Set the Identity of this token
    token.identity = user_id

    # Grant access to Video
    grant = VideoGrant(room=room)
    token.add_grant(grant)
    # Serialize the token as a JWT
    jwt = token.to_jwt()
    print(jwt)

    return jwt
