from django.conf import settings
from django.db import models


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
    country = models.CharField(
        max_length=100,
        blank=True,
        help_text='Optional. Country to search in, written in full, e.g. "Nigeria". Leave empty to search everywhere.',
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        help_text='Optional. City or area, e.g. "Lagos". Leave empty to search the whole country, or everywhere if no country is set.',
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