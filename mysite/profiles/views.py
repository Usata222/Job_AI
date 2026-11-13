import os

from django_countries import countries
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Profile, Resume
from .serializers import ProfileSerializer, ResumeSerializer, ResumeUploadSerializer


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


def _display_name(name):
    """Make the user's file name safe to show: no folders, no control characters."""
    name = os.path.basename(name.replace('\\', '/'))
    name = ''.join(ch for ch in name if ch.isprintable())
    return name[:255] or 'resume'


class ResumeView(APIView):
    """The logged-in user's resume: upload (replaces the old one), view details, delete."""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_throttles(self):
        # Uploads get a much stricter limit than reading.
        if self.request.method == 'POST':
            self.throttle_scope = 'resume_upload'
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume is None:
            return Response({'detail': 'No resume uploaded.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResumeSerializer(resume).data)

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        upload = serializer.validated_data['file']

        resume = Resume.objects.filter(user=request.user).first()
        created = resume is None
        old_path = None
        if created:
            resume = Resume(user=request.user)
        else:
            old_path = resume.file.name

        resume.original_name = _display_name(upload.name)
        resume.size_bytes = upload.size
        resume.file = upload
        resume.save()

        if old_path and old_path != resume.file.name:
            resume.file.storage.delete(old_path)

        return Response(
            ResumeSerializer(resume).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def delete(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume is None:
            return Response({'detail': 'No resume uploaded.'}, status=status.HTTP_404_NOT_FOUND)
        resume.delete()  # the file on disk is removed too
        return Response(status=status.HTTP_204_NO_CONTENT)