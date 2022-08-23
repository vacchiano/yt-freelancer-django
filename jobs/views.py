from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from jobs.models import Freelancer, Business

def index(request):
    return HttpResponse("<h1>Freelancers</h1>")

class FreelancerListView(ListView):
    model = Freelancer

class FreelancerDetailView(DetailView):
    model = Freelancer

class FreelancerCreateView(LoginRequiredMixin, CreateView):
    model = Freelancer
    fields = ['name', 'profile_pic', 'tagline', 'bio', 'website']
    success_url = reverse_lazy('freelancer-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(FreelancerCreateView, self).form_valid(form)

class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    fields = ['name', 'profile_pic', 'bio']
    success_url = reverse_lazy('freelancer-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BusinessCreateView, self).form_valid(form)

@login_required
def handle_login(request):
    if request.user.get_freelancer() or request.user.get_business():
        return redirect(reverse_lazy('freelancer-list'))

    return render(request, 'jobs/choose_account.html', {})