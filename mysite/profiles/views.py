from django_countries import countries
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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


class CountryListView(APIView):
    """Every country the profile can use, "Worldwide" first, then A to Z."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            [{'code': c.code, 'name': str(c.name)} for c in countries]
        )