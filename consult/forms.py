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
                                                                                       'value': use['Uses_id'],
                                                                                   }))
