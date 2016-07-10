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


class ContactForm(forms.Form):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
                           error_messages={'required': 'This field is required.'})
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': 'Enter your massage for us here. We will get back to you within 1 business day.',
               'class': 'form-control', 'rows': '7'}))

    def clean_name(self):
        data = self.cleaned_data['name']
        if not data.replace(' ', '').isalpha():
            raise forms.ValidationError("Name should contain only letters and space .")
