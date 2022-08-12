from django.shortcuts import render

# Add the following import

# Define the home view
def home(request):
  return render(request, 'home.html')