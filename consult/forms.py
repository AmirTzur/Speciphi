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
    name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone = forms.RegexField(required=False, regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                                 "Phone number must be entered in the format: '+972555555', " +
                                 "Up to 15 digits allowed."))
    message = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Your name:"
        self.fields['email'].label = "Email address:"
        self.fields['phone'].label = "Phone number:"
        self.fields['message'].label = "Message:"
