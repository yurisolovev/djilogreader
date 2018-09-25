from django.forms import ModelForm, Form, ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


from django_countries.widgets import CountrySelectWidget
from sorl.thumbnail.fields import ImageFormField

from .models import Profile, Note, Log


# ------------ Model forms ------------
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['birthdate', 'country', 'info', 'dron_model']
        widgets = {'country': CountrySelectWidget()}

    def clean_birthdate(self):
        data = self.cleaned_data['birthdate']
        if data >= timezone.datetime.date(timezone.now()):
            raise ValidationError("Дата должна быть не позднее текущей даты")
        return data


class UserNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('user', 'title', 'body')


class UploadLogForm(ModelForm):
    class Meta:
        model = Log
        fields = ('user', 'log_file')



# ------------ Forms ------------
class ProfileImageForm(Form):
    profile_photo = ImageFormField()
