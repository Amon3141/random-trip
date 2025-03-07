from django.contrib.auth.forms import UserCreationForm
from randomtrip.models import CustomUser

# a form to create a new CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields 