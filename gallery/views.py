from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from .models import Photo
from .forms import PhotoCreateForm
import reptopia
import logging


logger = logging.getLogger('reptopia.log')


class PhotoListView(ListView):
    model = Photo
    template_name = 'gallery/photo_list.html.j2'
    context_object_name = 'photo_list'
    paginate_by = 20

    def get_queryset(self):
        return Photo.objects.all()


class PhotoCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'gallery/photo_form.html.j2'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
