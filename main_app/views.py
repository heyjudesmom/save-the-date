from unicodedata import name
from .models import Activity, Date, Photo
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Now can decorate any user centric functions with @login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import os
import uuid
import boto3
# Now can apply LoginRequiredMixin to any CBV

# Add the following import

# Define the home view
def landing(request):
  return render(request, 'landing.html')


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
  return redirect('activity')

@login_required
def dates_index(request):
  # dates = Date.objects.all()
  dates = Date.objects.filter(user=request.user)
  return render(request, 'dates/index.html', {'dates': dates})

@login_required
def dates_detail(request, date_id):
  date = Date.objects.get(id=date_id)
  all_activities = Activity.objects.all()
  id_list = date.activities.all().values_list('id')
  not_on_date = Activity.objects.exclude(id__in=id_list)
  return render(request, 'dates/detail.html', {'date': date, 'all_activities': all_activities, 'not_on_date': not_on_date})


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

def add_photo(request, date_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, date_id=date_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', date_id=date_id)

@login_required
def assoc_activity(request, date_id, activity_id):
  Date.objects.get(id=date_id).activities.add(activity_id)
  return redirect('detail', date_id=date_id)

@login_required
def unassoc_activity(request, date_id, activity_id):
  Date.objects.get(id=date_id).activities.remove(activity_id)
  return redirect('detail', date_id=date_id)

def activity(request):
  a = requests.get('http://www.boredapi.com/api/activity/').json()
  all_activities = Activity.objects.all()
  return render(request, 'activity.html', {'a': a, 'all_activities': all_activities})

class ActivityDelete(DeleteView):
  model = Activity
  success_url = '/activity/'


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
