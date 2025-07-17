from rest_framework import serializers
from engagement.models import Profile, Alert

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['creator']

class AlertSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Alert
        fields = '__all__'

    def perform_update(self, serializer):
        instance = self.get_object()
        old_milestone = instance.milestone
        new_milestone = self.request.data.get('milestone')
        updated_alert = serializer.save()
        if new_milestone and int(new_milestone) > old_milestone:
            updated_alert.triggered = False
            updated_alert.save(update_fields=['triggered'])

