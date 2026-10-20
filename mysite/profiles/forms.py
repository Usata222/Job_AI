from django import forms
from django.conf import settings
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


class SearchableSelect(forms.Select):
    """A normal dropdown with a search box, using the select2 that ships with Django admin.

    If the script fails to load, it still works as a plain dropdown.
    """

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=(
                f'admin/js/vendor/jquery/jquery{extra}.js',
                f'admin/js/vendor/select2/select2.full{extra}.js',
                'admin/js/jquery.init.js',
            ),
            css={
                'screen': (
                    f'admin/css/vendor/select2/select2{extra}.css',
                    'admin/css/autocomplete.css',
                )
            },
        )

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        element_id = (attrs or {}).get('id') or f'id_{name}'
        return format_html(
            "{}<script>django.jQuery(function () {{"
            " django.jQuery('#{}').select2({{width: '22em'}}); }});</script>",
            html,
            element_id,
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
        widgets = {'country': SearchableSelect}