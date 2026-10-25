from rest_framework import generics, permissions

from .models import Profile
from .serializers import ProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Read the profile, or change some of its fields. No PUT: a profile is
    # never replaced wholesale, only updated field by field.
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile