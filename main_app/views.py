from unicodedata import name
from .models import Activity, Date
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Now can decorate any user centric functions with @login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import asyncio
# Now can apply LoginRequiredMixin to any CBV

# Add the following import

# Define the home view
def landing(request):
  return render(request, 'landing.html')

def activity(request):
  a = requests.get('http://www.boredapi.com/api/activity/').json()
  return render(request, 'activity.html', {'a': a})

def create_activity(request):
  all_activities = {}
  key = request.GET.get('key')
  if key:
    a = requests.get(f'http://www.boredapi.com/api/activity?key={key}').json()
    activity_data = Activity( 
      name = a['activity'],
      type = a['type'],
      participants = a['participants'],
      price = a['price'],
      key = a['key'],
    )
    activity_data.save()
    print(activity_data)
    all_activities = Activity.objects.all()
    print(all_activities)
  # filter(user=request.user)
  return redirect('activity', {'all_activities': all_activities})

@login_required
def dates_index(request):
  # dates = Date.objects.all()
  dates = Date.objects.filter(user=request.user)
  return render(request, 'dates/index.html', {'dates': dates})

@login_required
def dates_detail(request, date_id):
  date = Date.objects.get(id=date_id)
  return render(request, 'dates/detail.html', {'date': date})


class DateCreate(CreateView, LoginRequiredMixin):
  model = Date
  fields = ['title', 'date', 'notes', 'company', 'location']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class DateUpdate(LoginRequiredMixin, UpdateView):
  model = Date
  fields = ['title', 'date', 'notes', 'company', 'location']

class DateDelete(LoginRequiredMixin, DeleteView):
  model = Date
  success_url= '/dates/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('dates')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
