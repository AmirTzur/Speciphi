from django import forms

from consult.models import Affiliations


class AffiliationsForm(forms.Form):
    class Meta:
        # fields = []
        # widgets = {}
        # affs = Affiliations.objects.all()
        # for aff in affs:
        #     fields.append(aff.name)
        #     widgets.update({
        #         aff.name: forms.CheckboxInput(attrs={
        #             'id': aff.name+'_box',
        #             'name': aff.name,
        #             'class': 'checkbox',
        #             'required': False
        #         })
        #     })
        fields = [
            'Student',
            'Gamer'
        ]
        widgets = {
            'Student': forms.CheckboxInput(attrs={
                'id': 'Student_box',
                'name': 'Student',
                'class': 'checkbox',
                'required': False,
            }),
            'Gamer': forms.CheckboxInput(attrs={
                'id': 'Gamer_box',
                'name': 'Gamer',
                'class': 'checkbox',
                'required': False,
            })
        }


        #
        # class SignupForm(forms.Form):
        #     email = forms.EmailField(label='Email', required=True)
        #
        #     class Meta:
        #         model = get_user_model()
        #
        #     def save(self, user):
        #         user.email = self.cleaned_data['email']
        #         user.save()

        # class RegisterForm(UserCreationForm):
        #     class Meta:
        #         model = UserProfile
        #         fields = ("username", "email")

        # http://stackoverflow.com/questions/23956288/django-all-auth-email-required
