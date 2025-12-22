package com.example.informer

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.google.firebase.messaging.FirebaseMessaging

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            Log.d("BootReceiver", "Device booted, initializing FCM")

            // Initialize Firebase Messaging
            FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    Log.d("BootReceiver", "FCM token retrieved: ${task.result}")
                } else {
                    Log.e("BootReceiver", "FCM token fetch failed", task.exception)
                }
            }
        }
    }
}