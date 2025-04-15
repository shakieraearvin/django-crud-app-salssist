from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import License, Checklist, Accountant

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from datetime import date
from django.db.models import Sum

@login_required
def home(request):
    licenses = License.objects.filter(user=request.user)
    checklists = Checklist.objects.filter(user=request.user)
    accountants = Accountant.objects.filter(user=request.user)

    # Summarize accounting
    income_total = accountants.filter(type='I', date__month=date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = accountants.filter(type='E', date__month=date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'home.html', {
        'license_count': licenses.count(),
        'checklist_required': checklists.filter(status='R').count(),
        'checklist_progress': checklists.filter(status='I').count(),
        'income_total': income_total,
        'expense_total': expense_total
    })


@login_required
def dashboard(request):
    user = request.user

    total_licenses = License.objects.filter(user=user).count()

    today = timezone.now().date()
    soon = today + timedelta(days=30)
    expiring_licenses = License.objects.filter(user=user, exp_date__range=[today, soon]).count()

    total_checklist = Checklist.objects.filter(user=user).count()
    completed_checklist = Checklist.objects.filter(user=user, status='C').count()

    income_items = Accountant.objects.filter(user=user, type='I')
    expense_items = Accountant.objects.filter(user=user, type='E')

    income_total = income_items.aggregate(total=Sum('amount'))['total'] or 0
    expense_total = expense_items.aggregate(total=Sum('amount'))['total'] or 0
    net_total = income_total - expense_total

    context = {
        'total_licenses': total_licenses,
        'expiring_licenses': expiring_licenses,
        'total_checklist': total_checklist,
        'completed_checklist': completed_checklist,
        'income_total': income_total,
        'expense_total': expense_total,
        'net_total': net_total,
        'income_items': income_items,
        'expense_items': expense_items,
    }

    return render(request, 'dashboard.html', context)


class LicenseList(LoginRequiredMixin, ListView):
    model = License
    template_name = 'licenses/index.html'
    context_object_name = 'licenses'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New License'
        context['cancel_url'] = '/licenses/'
        return context

       
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
    context_object_name = 'checklists'

    def get_queryset(self):
        queryset = Checklist.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            print("QUERYSET:", queryset)
        return queryset
        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        return context




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
    context_object_name = 'accountants'

    def get_queryset(self):
        queryset = Accountant.objects.filter(user=self.request.user)

        type_filter = self.request.GET.get('type')
        sort = self.request.GET.get('sort')

        if type_filter in ['I', 'E']:
            queryset = queryset.filter(type=type_filter)

        if sort == 'amount':
            queryset = queryset.order_by('-amount')
        elif sort == 'date':
            queryset = queryset.order_by('-date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_type'] = self.request.GET.get('type', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        return context
    
        print("Filtered transactions:", queryset)



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Transaction'
        context['cancel_url'] = f"/accounting/{self.object.pk}/"
        return context


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
            return redirect('license-index') 
        else:
            error_message = 'Invalid sign up - please try again.'
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form,
        'error_message': error_message
    })
