from django.shortcuts import render, redirect
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
  activity = requests.get('http://www.boredapi.com/api/activity/').json()['activity']
  return render(request, 'activity.html', {'activity': activity})

@login_required
def dates(request):
  return render(request, 'dates.html')

@login_required
def create_date(request):
  pass

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
