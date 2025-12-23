import azure.functions as func
import logging
import json
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

FCM_TOKEN = os.environ.get('FCM_TOKEN')
PROJECT_ID = os.environ.get('PROJECT_ID')
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="SendNotification")
def SendNotification(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('SendNotification function triggered.')
    
    try:
        # Get message from request body
        req_body = req.get_json()
        message = req_body.get('message', 'New job listing found!')
        
        # Send FCM notification
        result = send_fcm_notification(message)
        
        if result:
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "Notification sent"}),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Failed to send notification"}),
                status_code=500,
                mimetype="application/json"
            )
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_access_token():
    """Get access token from service account."""
    credentials = service_account.Credentials.from_service_account_file(
        'firebase-credentials.json',
        scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = Request()
    credentials.refresh(request)
    return credentials.token

def send_fcm_notification(message):
    """Send FCM notification to device."""
    try:
        access_token = get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json; UTF-8',
        }
        
        payload = {
            'message': {
                'token': FCM_TOKEN,
                'data': {
                    'message': message
                },
                'android': {
                    'priority': 'high'  # This ensures immediate delivery
                }
            }
        }
        
        url = f'https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send'
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            logging.info(f"Notification sent successfully: {message}")
            return True
        else:
            logging.error(f"FCM error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"Error sending FCM: {str(e)}")
        return False
