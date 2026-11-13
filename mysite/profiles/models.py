import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_countries.fields import CountryField


class Profile(models.Model):
    class WorkArrangement(models.TextChoices):
        REMOTE = 'remote', 'Remote'
        HYBRID = 'hybrid', 'Hybrid'
        ONSITE = 'onsite', 'On-site (office)'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry level'
        JUNIOR = 'junior', 'Junior'
        MID = 'mid', 'Mid level'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead / Manager'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    target_role = models.CharField(
        max_length=150,
        blank=True,
        help_text='The job title or keyword to search for, e.g. "Backend Developer".',
    )
    country = CountryField(
        default='WW',
        help_text='The country to search for jobs in. Choose Worldwide to search every country.',
    )
    work_arrangements = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "Where you are willing to work. "
            "Remote: from home, no office. "
            "Hybrid: some days at an office, some days from home. "
            "On-site: at the employer's office every working day. "
            "Tick every option you would accept."
        ),
    )
    employment_types = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "The kinds of job you want. "
            "Full-time: a standard permanent job. "
            "Part-time: fewer hours than full-time. "
            "Contract: a fixed period or project, not permanent staff. "
            "Internship: a short training role, usually for students or new graduates. "
            "Tick every option you would accept."
        ),
    )
    experience_level = models.CharField(
        max_length=20, choices=ExperienceLevel.choices, blank=True
    )
    years_of_experience = models.PositiveSmallIntegerField(null=True, blank=True)
    min_monthly_salary_usd = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Optional. The lowest salary you would accept, per month, in US dollars (USD).',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.email}'


def resume_upload_path(instance, filename):
    """Store under a generated name. The name the user sent is never used on disk."""
    extension = os.path.splitext(filename)[1].lower()
    return f'resumes/{instance.user_id}/{uuid.uuid4().hex}{extension}'


class Resume(models.Model):
    class TextStatus(models.TextChoices):
        PENDING = 'pending', 'Not read yet'
        EXTRACTED = 'extracted', 'Text extracted'
        NO_TEXT = 'no_text', 'No readable text found'
        FAILED = 'failed', 'Could not be read'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resume',
    )
    file = models.FileField(upload_to=resume_upload_path, max_length=255)
    original_name = models.CharField(max_length=255)  # for display only
    size_bytes = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now=True)
    extracted_text = models.TextField(blank=True)
    text_status = models.CharField(
        max_length=20, choices=TextStatus.choices, default=TextStatus.PENDING
    )

    def __str__(self):
        return f'Resume of {self.user.email}'


@receiver(post_delete, sender=Resume)
def delete_resume_file(sender, instance, **kwargs):
    """Remove the file from disk whenever its database row is deleted."""
    if instance.file:
        instance.file.delete(save=False)