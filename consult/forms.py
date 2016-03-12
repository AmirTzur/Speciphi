import django.forms


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
