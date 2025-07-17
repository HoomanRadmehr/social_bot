from django.utils import timezone
from datetime import timedelta

from engagement.models import FollowerCountSnapshot

def get_top_follower_changes(user, platform=None, hours=24, limit=5):
    time_threshold = timezone.now() - timedelta(hours=hours)

    queryset = FollowerCountSnapshot.objects.filter(
        timestamp__gte=time_threshold,
        profile__creator=user,
    )

    if platform:
        queryset = queryset.filter(profile__platform=platform)

    snapshots = queryset.order_by('profile', '-timestamp').distinct('profile')

    changes = []
    for snap in snapshots:
        old_snap = FollowerCountSnapshot.objects.filter(
            profile=snap.profile,
            timestamp__lt=time_threshold
        ).order_by('-timestamp').first()

        old_count = old_snap.follower_count if old_snap else 0
        diff = snap.follower_count - old_count
        changes.append({'profile': snap.profile, 'change': diff})

    top_gains = sorted(changes, key=lambda x: x['change'], reverse=True)[:limit]
    top_losses = sorted(changes, key=lambda x: x['change'])[:limit]

    return {'top_gains': top_gains, 'top_losses': top_losses}
