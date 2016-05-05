from django import forms


class AffiliationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        Affiliations_dict = kwargs.pop('Affiliations_dict')
        super(AffiliationsForm, self).__init__(*args, **kwargs)
        for aff in Affiliations_dict:
            self.fields[aff.name] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                'id': aff.name + '_box',
                'name': aff.name,
                'value': aff.id,
            }))
