from django import forms
from collections import OrderedDict

class AffiliationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        affiliations_dict = kwargs.pop('affiliations_dict')
        super(AffiliationsForm, self).__init__(*args, **kwargs)
        for aff in affiliations_dict:
            self.fields[aff['name']] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                'id': aff['name'] + '_box',
                'name': aff['name'],
                'value': aff['id'],
            }))


class UsesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        uses_dict = kwargs.pop('uses_dict')
        super(UsesForm, self).__init__(*args, **kwargs)
        for use in uses_dict:
            self.fields[use['Uses_name'] + str(use['value'])] = forms.BooleanField(required=False,
                                                                                   widget=forms.CheckboxInput(attrs={
                                                                                       'id': str(
                                                                                           use['Uses_id']) + '_' + str(
                                                                                           use['value']),
                                                                                       'name': use['Uses_name'],
                                                                                       'value': use['value'],
                                                                                   }))


# Import filtering fields (categories and types) from db
class FilterForm(forms.Form):
    """

    """

    def __init__(self, *args, **kwargs):
        filters_list = kwargs.pop('filters_list', {})
        filters_optional = kwargs.pop('filters_optional', {})
        filters_selected = kwargs.pop('filters_selected', {})
        super(FilterForm, self).__init__(*args, **kwargs)
        for field_key, field_vals in filters_list.items():
            for spec in field_vals:
                if spec in filters_optional[str(field_key)]:
                    if spec in filters_selected[str(field_key)]:
                        self.fields[str(field_key) + "_" + str(spec)] = forms.BooleanField(
                            required=False,
                            initial=True,
                            label=str(spec),
                            widget=forms.CheckboxInput(attrs={
                                'id': str(field_key) + "-" + str(spec),
                                'name': str(spec),
                                'value': str(field_key) + "-" + str(spec),
                                'disabled': False,
                            }))
                    else:
                        self.fields[str(field_key) + "_" + str(spec)] = forms.BooleanField(
                            required=False,
                            initial=False,
                            label=str(spec),
                            widget=forms.CheckboxInput(attrs={
                                'id': str(field_key) + "-" + str(spec),
                                'name': str(spec),
                                'value': str(field_key) + "-" + str(spec),
                                'disabled': False,
                            }))
                else:
                    self.fields[str(field_key) + "_" + str(spec)] = forms.BooleanField(
                        required=False,
                        initial=False,
                        label=str(spec),
                        widget=forms.CheckboxInput(attrs={
                            'id': str(field_key) + "-" + str(spec),
                            'name': str(spec),
                            'value': str(field_key) + "-" + str(spec),
                            'disabled': True,
                        }))


