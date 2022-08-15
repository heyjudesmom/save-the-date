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
# Now can apply LoginRequiredMixin to any CBV

# Add the following import

# Define the home view
def landing(request):
  return render(request, 'landing.html')

def activity(request):
  a = requests.get('http://www.boredapi.com/api/activity/').json()
  return render(request, 'activity.html', {'a': a})

def create_activity(request):
  a = requests.get('http://www.boredapi.com/api/activity/').json()
  for x in a:
    activity_data = Activity( 
      name = x['activity'],
      type = x['type'],
      participants = x['participants'],
      price = x['price'],
    )

    activity_data.save()
    all_activities = Activity.objects.filter(user=request.user)
    return redirect(request, 'activity.html', {'all_activities': all_activities})

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
