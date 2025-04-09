from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import License, Checklist, Accountant


# Create your views here.
class LicenseList(LoginRequiredMixin, ListView):
    model = License
    template_name = 'licenses/index.html'

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)


class LicenseDetail(LoginRequiredMixin, DetailView):
    model = License
    template_name = 'licenses/detail.html'

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)


class LicenseCreate(LoginRequiredMixin, CreateView):
    model = License
    fields = ['type', 'cost', 'issue_date', 'exp_date', 'status', 'document']
    template_name = 'licenses/form.html'
    success_url = '/licenses/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LicenseUpdate(LoginRequiredMixin, UpdateView):
    model = License
    fields = ['type', 'cost', 'issue_date', 'exp_date', 'status', 'document']
    template_name = 'licenses/form.html'
    success_url = '/licenses/'

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)


class LicenseDelete(LoginRequiredMixin, DeleteView):
    model = License
    template_name = 'licenses/delete_confirm.html'
    success_url = '/licenses/'

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)


class ChecklistList(LoginRequiredMixin, ListView):
    model = Checklist
    template_name = 'checklists/index.html'

    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)


class ChecklistDetail(LoginRequiredMixin, DetailView):
    model = Checklist
    template_name = 'checklists/detail.html'

    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)


class ChecklistCreate(LoginRequiredMixin, CreateView):
    model = Checklist
    fields = ['title', 'status', 'notes', 'date']
    template_name = 'checklists/form.html'
    success_url = '/checklists/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChecklistUpdate(LoginRequiredMixin, UpdateView):
    model = Checklist
    fields = ['title', 'status', 'notes', 'date']
    template_name = 'checklists/form.html'
    success_url = '/checklists/'

    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)


class ChecklistDelete(LoginRequiredMixin, DeleteView):
    model = Checklist
    template_name = 'checklists/delete_confirm.html'
    success_url = '/checklists/'

    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)


class AccountantList(LoginRequiredMixin, ListView):
    model = Accountant
    template_name = 'accountants/index.html'

    def get_queryset(self):
        return Accountant.objects.filter(user=self.request.user)


class AccountantDetail(LoginRequiredMixin, DetailView):
    model = Accountant
    template_name = 'accountants/detail.html'

    def get_queryset(self):
        return Accountant.objects.filter(user=self.request.user)


class AccountantCreate(LoginRequiredMixin, CreateView):
    model = Accountant
    fields = ['type', 'name', 'amount', 'date', 'source', 'notes', 'receipt']
    template_name = 'accountants/form.html'
    success_url = '/accounting/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountantUpdate(LoginRequiredMixin, UpdateView):
    model = Accountant
    fields = ['type', 'name', 'amount', 'date', 'source', 'notes', 'receipt']
    template_name = 'accountants/form.html'
    success_url = '/accounting/'

    def get_queryset(self):
        return Accountant.objects.filter(user=self.request.user)


class AccountantDelete(LoginRequiredMixin, DeleteView):
    model = Accountant
    template_name = 'accountants/delete_confirm.html'
    success_url = '/accounting/'

    def get_queryset(self):
        return Accountant.objects.filter(user=self.request.user)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('license-index')  # or use 'home' if you create one
        else:
            error_message = 'Invalid sign up - please try again.'
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form,
        'error_message': error_message
    })
