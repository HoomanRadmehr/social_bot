from rest_framework import generics, permissions
from accounts.serializers import UserProfileSerializer

class UpdateTelegramInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile
