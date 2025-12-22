package com.example.informer

import android.media.AudioAttributes
import android.media.MediaPlayer
import android.util.Log
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class InformerFirebaseMessagingService : FirebaseMessagingService() {

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        Log.d("FCM", "Message received from: ${message.from}")

        // Play loud sound at MEDIA volume
        playAlertSound()
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d("FCM", "New FCM token: $token")
        // Token will be displayed in MainActivity
    }

    private fun playAlertSound() {
        try {
            val mediaPlayer = MediaPlayer.create(this, R.raw.alert)
            mediaPlayer?.setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .build()
            )
            mediaPlayer?.setOnCompletionListener { mp ->
                mp.release()
            }
            mediaPlayer?.start()
            Log.d("FCM", "Playing alert sound")
        } catch (e: Exception) {
            Log.e("FCM", "Error playing sound: ${e.message}")
        }
    }
}