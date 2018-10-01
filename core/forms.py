from django.forms import ModelForm, Form, ValidationError
from django.forms.fields import CharField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.template import loader
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from django_countries.widgets import CountrySelectWidget
from sorl.thumbnail.fields import ImageFormField

from .tasks import send_reset_password_email_to_user

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
        if data and data >= timezone.datetime.date(timezone.now()):
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


class ChangeUsernameForm(Form):
    new_username = CharField(max_length=150,
                             validators=[RegexValidator(regex=r'^[\w.@+-]+$',
                                                        message=_(
                                                            'Enter a valid username. This value may contain only '
                                                            'letters, numbers, and @/./+/-/_ characters.'
                                                        ),
                                                        flags=0)],
                             label='Новое имя пользователя', required=True)


class ConfirmUsernameForm(Form):
    username_confirm = CharField(max_length=150, required=True, label='Имя пользователя')


class UserPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        send_reset_password_email_to_user.delay(subject, body, from_email, to_email,
                                                context, html_email_template_name)
