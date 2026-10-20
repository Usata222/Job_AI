from django import forms
from django.utils.html import format_html

from .models import Profile

# Runs in the browser when a box is ticked or unticked: rewrites the closed
# dropdown's text to list the ticked options.
UPDATE_SUMMARY = (
    "this.querySelector('summary').textContent = "
    "Array.from(this.querySelectorAll('input:checked'))"
    ".map(i => i.parentElement.textContent.trim()).join(', ') "
    "|| 'Select one or more'"
)

SUMMARY_STYLE = (
    "display:block;cursor:pointer;max-width:22em;padding:6px 10px;"
    "border:1px solid var(--border-color, #ccc);border-radius:4px;"
)


class DropdownCheckboxes(forms.CheckboxSelectMultiple):
    """A dropdown that opens into tick boxes, so several options can be chosen."""

    def render(self, name, value, attrs=None, renderer=None):
        selected = [str(v) for v in (value or [])]
        labels = [str(label) for key, label in self.choices if str(key) in selected]
        summary = ', '.join(labels) or 'Select one or more'
        boxes = super().render(name, value, attrs, renderer)
        return format_html(
            '<details onchange="{}"><summary style="{}">{}</summary>{}</details>',
            UPDATE_SUMMARY,
            SUMMARY_STYLE,
            summary,
            boxes,
        )


class ProfileAdminForm(forms.ModelForm):
    work_arrangements = forms.MultipleChoiceField(
        choices=Profile.WorkArrangement.choices,
        widget=DropdownCheckboxes,
        required=False,
        help_text=Profile._meta.get_field('work_arrangements').help_text,
    )
    employment_types = forms.MultipleChoiceField(
        choices=Profile.EmploymentType.choices,
        widget=DropdownCheckboxes,
        required=False,
        help_text=Profile._meta.get_field('employment_types').help_text,
    )

    class Meta:
        model = Profile
        fields = '__all__'