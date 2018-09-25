import os


from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator

from .viewmixins import OnlyCurrentUserAccessMixin
from .forms import UserForm, ProfileForm, ProfileImageForm, UserNoteForm, UploadLogForm
from .models import Note, Log
from .utils import get_images_list


class IndexRedirectView(RedirectView, View):
    """ Redirect 301 from '/' to '/<username>/' if user is authenticated
        if it isn't - to '/accounts/login/'

    """
    permanent = True
    pattern_name = 'core:index'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            kwargs['username'] = self.request.user.username
        else:
            self.pattern_name = 'core:login'
        return super().get_redirect_url(*args, **kwargs)


class UserLoginView(LoginView):
    """ Login """
    username = ''

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('core:index', args=[self.username])

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        self.username = form.get_user().username
        return HttpResponseRedirect(self.get_success_url())


class RegistrationView(View):
    """ Registration """
    template_name = 'registration/register.html'

    def get(self, request, * args, ** kwargs):
        form = UserCreationForm()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, * args, ** kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('core:edit-profile', args=[form.cleaned_data['username']]))
        return render(request, template_name=self.template_name, context={'form': form})


class IndexView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Index page """
    form = UploadLogForm
    template_name = 'core/index.html'

    def get(self, request, * args, ** kwargs):
        form = self.form()
        all_logs = Log.objects.filter(user_id=request.user.id).order_by('-timestamp')
        paginator = Paginator(all_logs, 10)
        page = request.GET.get('page')
        logs = paginator.get_page(page)
        context = {'form': form, 'logs': logs}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data = {'is_valid': True}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class LogView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, DetailView):
    model = Log
    template_name = 'core/log.html'
    context_object_name = 'log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kml'] = 'http://openflights.org/demo/openflights-sample.kml'
        context['images'] = get_images_list(context['log'].log_directory)
        context['rel_path'] = os.path.split(context['log'].kml_file.name)[0]
        return context


class DeleteLog(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    model = Log

    def post(self, request, *args, **kwargs):
        log_id = request.POST.get('log_id')
        if log_id:
            try:
                log = Log.objects.get(pk=log_id)
            except Log.DoesNotExist:
                messages.error(request, 'Объект не существует или был удалена')
            else:
                log.delete_log_files()
                log.delete()
        return redirect(reverse('core:index', args=[request.user.get_username()]))


class ProfileView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ User profile view """
    form_note = UserNoteForm
    template_name = 'core/profile.html'

    def get(self, request, * args, ** kwargs):
        form_note = self.form_note()
        all_notes = Note.objects.filter(user_id=request.user.id).order_by('-timestamp')
        paginator = Paginator(all_notes, 5)
        page = request.GET.get('page')
        notes = paginator.get_page(page)
        return render(request, self.template_name, {'form_note': form_note, 'notes': notes})


class EditProfileView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Edit Profile """
    form_user = UserForm
    form_profile = ProfileForm
    form_image = ProfileImageForm
    template_name = 'core/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form_user = self.form_user(instance=request.user)
        form_profile = self.form_profile(instance=request.user.profile)
        form_image = self.form_image()
        return render(request, self.template_name, {'form_user': form_user, 'form_profile': form_profile,
                                                    'form_image': form_image})

    def post(self, request, *args, **kwargs):
        form_user = self.form_user(request.POST, instance=request.user)
        form_profile = self.form_profile(request.POST, instance=request.user.profile)
        form_image = self.form_image()
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
            return redirect(reverse('core:profile', args=[request.user.username]))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки')
        return render(request, self.template_name, {'form_user': form_user, 'form_profile': form_profile,
                                                    'form_image': form_image})


class EditProfileImageView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Upload Profile Photo, only POST """
    form_image = ProfileImageForm

    def post(self, request, *args, **kwargs):
        form_image = self.form_image(request.POST, request.FILES)
        if form_image.is_valid():
            if request.user.profile.profile_photo:
                request.user.profile.profile_photo.delete()
            request.user.profile.profile_photo = form_image.cleaned_data['profile_photo']
            request.user.profile.save()
        else:
            messages.error(request, 'Файл не выбран или имеет недопустимый формат')
        return redirect(reverse('core:edit-profile', args=[request.user.username]))


class DeleteProfileImageView(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Delete Profile Photo, only POST """

    def post(self, request, *args, **kwargs):
        request.user.profile.profile_photo.delete()
        return redirect(reverse('core:edit-profile', args=[request.user.username]))


class CreateNote(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Create user note """
    form_note = UserNoteForm

    def post(self, request, *args, **kwargs):
        form_note = self.form_note(request.POST)
        if form_note.is_valid():
            form_note.save()
        return redirect(reverse('core:profile', args=[request.user.username]))


class EditNote(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Edit user note """
    form_note = UserNoteForm

    def post(self, request, *args, **kwargs):
        note_id = request.POST.get('note_id')
        if note_id:
            try:
                note = Note.objects.get(pk=note_id)
            except Note.DoesNotExist:
                messages.error(request, 'Заметка не существует или была удалена')
                return redirect(reverse('core:profile', args=[request.user.username]))
            else:
                form_note = self.form_note(request.POST, instance=note)
                if form_note.is_valid():
                    form_note.save()
        return redirect(reverse('core:profile', args=[request.user.username]))


class DeleteNote(LoginRequiredMixin, OnlyCurrentUserAccessMixin, View):
    """ Delete user note """
    def post(self, request, *args, **kwargs):
        note_id = request.POST.get('note_id')
        if note_id:
            try:
                note = Note.objects.get(pk=note_id)
            except Note.DoesNotExist:
                messages.error(request, 'Заметка не существует или была удалена')
            else:
                note.delete()
        return redirect(reverse('core:profile', args=[request.user.username]))
