from django import forms


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


# Import filtering field (categories and types) from db
class FilterForm(forms.Form):
    """

    """
    ff_data = []

    def __init__(self, *args, **kwargs):
        filtering_data = kwargs.get('filtering_data', {})
        super(FilterForm, self).__init__(*args, **kwargs)
        for field_key, field_val in filtering_data.items():
            self.fields[filter_field['Uses_name'] + str(filter_field['value'])] = forms.BooleanField(required=False,
                                                                                   widget=forms.CheckboxInput(attrs={
                                                                                       'id': str(
                                                                                           filter_field['Uses_id']) + '_' + str(
                                                                                           filter_field['value']),
                                                                                       'name': filter_field['Uses_name'],
                                                                                       'value': filter_field['value'],
                                                                                   }))

