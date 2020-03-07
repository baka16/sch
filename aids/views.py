from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import *
from .models import *

# Create your views here.

class ClassRoomListView(ListView):
    model = ClassRoom
    # template_name = ".html"


class ClassRoomCreateView(CreateView):
    form_class = ClassRoomCreateForm
    # model = ClassRoom
    template_name = "aids/classroom_form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        # instance.owner = self.request.user
        return super(ClassRoomCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ClassRoomCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Classroom'
        return context



class ClassRoomDetailView(DetailView):
    model = ClassRoom
    # template_name = ".html"


class ClassRoomDeleteView(DeleteView):
    model = ClassRoom
    # template_name = ".html"


class SchoolCreateView(CreateView):
    model = SchoolInfo
    # template_name = ".html"
