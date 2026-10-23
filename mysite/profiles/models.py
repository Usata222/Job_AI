from django.conf import settings
from django.db import models
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




    # jhb.jhuhoio'ihoi'oihoihoi