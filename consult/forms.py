from django import forms


class AffiliationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        affiliations_dict = kwargs.pop('affiliations_dict')
        super(AffiliationsForm, self).__init__(*args, **kwargs)
        for aff in affiliations_dict:
            self.fields[aff['name']] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                'name': aff['name'],
                'value': aff['id'],
            }))


class UsesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        uses_dict = kwargs.pop('uses_dict')
        super(UsesForm, self).__init__(*args, **kwargs)
        for use in uses_dict:
            self.fields[use['use_name'] + str(use['value'])] = forms.BooleanField(required=False,
                                                                                  widget=forms.CheckboxInput(attrs={
                                                                                      'id': str(
                                                                                          use['use_id']) + '_' + str(
                                                                                          use['value']),
                                                                                      'name': use['use_name'],
                                                                                      'value': use['value'],
                                                                                  }))


class QuestionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions_dict = kwargs.pop('questions_dict')
        super(QuestionsForm, self).__init__(*args, **kwargs)
        for que in questions_dict:
            self.fields[que['question_header'] + str(que['answer_id'])] = forms.BooleanField(required=False,
                                                                                             widget=forms.CheckboxInput(
                                                                                                 attrs={
                                                                                                     'value': str(que['question_id']) + "_" + str(que['answer_id']),
                                                                                                     'name': str(que['answer_name']),
                                                                                                     'type': 'radio',
                                                                                                 }))


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
