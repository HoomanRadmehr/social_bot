import asyncio
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from engagement.models import Profile, Alert, FollowerCountSnapshot
from services.platforms.telegram import send_telegram_alert

class Command(BaseCommand):
    help = 'Checks follower counts and triggers milestone alerts.'

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Starting follower count check...")

        async def run_checks():
            tasks = [self.check_profile(profile) for profile in Profile.objects.all()]
            await asyncio.gather(*tasks)

        asyncio.run(run_checks())
        self.stdout.write(f"✅ Follower check completed at {timezone.now()}")

    async def check_profile(self, profile):
        await asyncio.sleep(0.1) 
        change = random.randint(-20, 50)
        new_count = max(0, profile.follower_count + change)

        if new_count != profile.follower_count:
            profile.follower_count = new_count
            profile.save(update_fields=['follower_count', 'last_updated'])
            FollowerCountSnapshot.objects.create(profile=profile, follower_count=new_count)

        # 🚨 Check alerts for this profile
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
