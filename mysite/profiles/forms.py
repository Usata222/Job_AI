from django import forms

from .models import Profile


class ProfileAdminForm(forms.ModelForm):
    work_arrangements = forms.MultipleChoiceField(
        choices=Profile.WorkArrangement.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text=Profile._meta.get_field('work_arrangements').help_text,
    )
    employment_types = forms.MultipleChoiceField(
        choices=Profile.EmploymentType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text=Profile._meta.get_field('employment_types').help_text,
    )

    class Meta:
        model = Profile
        fields = '__all__'