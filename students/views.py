from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AdmissionCreateForm, PerformanceCreateForm
from .models import Admission, Performance


# class StudentListView(LoginRequiredMixin, ListView):
class StudentListView(ListView):
    model = Admission

    def get_queryset(self):
        queryset = Admission.objects.all()
        param = self.kwargs.get('param')
        if param:
            return queryset.filter(
                Q(academic_year__iexact=param) |
                Q(sex__iexact=param) |
                Q(class_enroll__iexact=param) |
                Q(level__iexact=param)
            )
        else:
            return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(StudentListView, self).get_context_data(
            *args, **kwargs)
        context['title'] = 'Students List'
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Admission
    queryset = Admission.objects.all()  # filter(stid='pk')
    # queryset = Admission.objects.get('pk'=stid)
    # performing = Admission.performance_set.filter(Admission__stid)
    # template_name = 'students/student_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentDetailView, self).get_context_data(
            *args, **kwargs)
        context['performing'] = self.admission.performance_set.all()
        context['title'] = 'Student Details'
        return context


class StudentCreateView(LoginRequiredMixin, CreateView):
    # class StudentCreateView(CreateView):
    form_class = AdmissionCreateForm
    template_name = 'students/form.html'
    # success_url = "/student/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(StudentCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(StudentCreateView, self).get_context_data(
            *args, **kwargs)
        context['title'] = 'Add Student'
        return context


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AdmissionCreateForm
    # template_name = 'student/detail-update.html'
    # success_url = "/student/"

    def get_context_data(self, *args, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(
            *args, **kwargs)
        name = self.get_object().first_name
        context['title'] = f'Update Student: {name}'
        return context

    def get_queryset(self):
        return Admission.objects.filter(stid='pk')
