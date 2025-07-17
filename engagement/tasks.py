# engagement/tasks.py

from celery import shared_task
from .models import Profile, Alert, FollowerCountSnapshot
from services.platforms.telegram import send_telegram_alert
import random
import asyncio
import logging

@shared_task
def check_follower_counts():
    logging.info("Checking follower counts...")

    for profile in Profile.objects.all():
        change = random.randint(-20, 50)
        new_count = max(0, profile.follower_count + change)

        if new_count != profile.follower_count:
            profile.follower_count = new_count
            profile.save(update_fields=['follower_count', 'last_updated'])
            FollowerCountSnapshot.objects.create(profile=profile, follower_count=new_count)

        alerts = Alert.objects.filter(profile=profile)

        for alert in alerts:
            if alert.triggered:
                if profile.follower_count < alert.milestone:
                    continue
            else:
                if profile.follower_count >= alert.milestone:
                    message = (
                        f"🎉 Milestone reached!\n"
                        f"User: @{profile.username} ({profile.platform})\n"
                        f"Reached: {alert.milestone} followers! 🎯"
                    )
                    chat_id = profile.creator.userprofile.telegram_chat_id
                    if chat_id:
                        asyncio.run(send_telegram_alert(message, chat_id))
                        alert.triggered = True
                        alert.save(update_fields=['triggered'])

    logging.info("Follower count check complete.")
