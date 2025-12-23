# Informer

A simple Android notification system that bypasses notification volume controls by playing alerts at media volume. Built for getting loud alerts for important events (like job postings) without cranking up notification volume for everything else.

## What It Does

- **Android app** receives Firebase Cloud Messaging (FCM) push notifications
- Plays custom sound at **media volume** (not notification volume)
- Works even when app is closed
- Auto-starts on phone reboot

## Architecture
```
Job Scraper → Azure Function → FCM → Android App → Loud Alert
```

- **Azure Function** (Python): HTTP endpoint that sends FCM pushes
- **Android App** (Kotlin): Receives FCM, plays alert sound

## Setup

### Android App

1. Open in Android Studio
2. Add your `google-services.json` from Firebase Console
3. Replace `alert.mp3` in `res/raw/` with your preferred sound
4. Build and install

### Azure Function

1. Create Firebase service account key
2. Deploy function via VS Code Azure Functions extension
3. Set environment variables in Azure:
   - `FCM_TOKEN`: Your device's FCM token (shown in app)
   - `PROJECT_ID`: Firebase project ID
4. Add `firebase-credentials.json` (excluded from git)

## Usage

POST to your function URL:
```json
{
  "message": "Your alert text here"
}
```

Phone plays loud alert instantly.

## Notes

Built during a conversation with Claude (Anthropic). Chat transcript: [link](https://claude.ai/share/f2122c14-fcb4-42da-a680-6f192bdc0e35)

FCM token and Firebase credentials intentionally excluded from source control.

On your phone make sure to set `Settings → Apps → Informer → Battery → "Unrestricted" (or "Don't optimize")`