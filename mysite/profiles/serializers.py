from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Profile


class ChoiceListField(serializers.MultipleChoiceField):
    """A list of allowed values, e.g. ["remote", "hybrid"], saved and returned as a list."""

    def to_internal_value(self, data):
        picked = super().to_internal_value(data)  # DRF gives back a set
        return [key for key in self.choices if key in picked]

    def to_representation(self, value):
        picked = set(value or [])
        return [key for key in self.choices if key in picked]


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    work_arrangements = ChoiceListField(
        choices=Profile.WorkArrangement.choices, required=False
    )
    employment_types = ChoiceListField(
        choices=Profile.EmploymentType.choices, required=False
    )
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'target_role',
            'country',
            'country_name',
            'work_arrangements',
            'employment_types',
            'experience_level',
            'years_of_experience',
            'min_monthly_salary_usd',
            'updated_at',
        )
        read_only_fields = ('updated_at',)
        extra_kwargs = {
            'years_of_experience': {'max_value': 60},
            'min_monthly_salary_usd': {'max_value': 1_000_000},
        }