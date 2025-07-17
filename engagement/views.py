from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from engagement.models import Profile, Alert
from engagement.permissions import IsOwnerPermission
from engagement.serializers import ProfileSerializer, AlertSerializer
from utils.functions import get_top_follower_changes

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username']
    filterset_fields = ['platform'] 
    ordering_fields = ['follower_count', 'last_updated']
    ordering = ['-last_updated']

    def get_queryset(self):
        return Profile.objects.filter(creator=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return Alert.objects.filter(profile__creator=self.request.user)
        
    def perform_update(self, serializer:AlertSerializer):
        instance = self.get_object()
        old_milestone = instance.milestone
        new_milestone = self.request.data.get('milestone')
        updated_alert = serializer.save()
        if new_milestone and int(new_milestone) > old_milestone:
            updated_alert.triggered = False
            updated_alert.save(update_fields=['triggered'])
    
class TopFollowerInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        platform = request.query_params.get('platform')
        data = get_top_follower_changes(user=request.user, platform=platform)
        result = {
            'top_gains': [
                {'username': item['profile'].username, 'change': item['change']}
                for item in data['top_gains']
            ],
            'top_losses': [
                {'username': item['profile'].username, 'change': item['change']}
                for item in data['top_losses']
            ],
        }
        return Response(result,status=status.HTTP_200_OK)
