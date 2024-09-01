from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
from main.models import shortened_link
from datetime import datetime, date
import string
import random

# Function to generate a random token of specified length
def createToken(length=7):
    characters = string.ascii_letters + string.digits

    # Get all existing tokens from the database
    all_tokens = shortened_link.objects.values_list('shortened_link', flat=True)
    
    # Create a new random token
    token = ''.join(random.choice(characters) for _ in range(length))
    
    # Ensure the token is unique
    if token in all_tokens:
        token = createToken()  # Recursively generate a new token if there's a collision
    
    return token

# View to handle successful token creation
def success_view(request, token):
    all_tokens = shortened_link.objects.values_list('shortened_link', flat=True)
    
    # Check if the token exists and render the appropriate template
    if token in all_tokens:
        return render(request, 'index/index_post.html', {'token': token})
    
    return render(request, "index/index.html")

# Main view to handle the creation of shortened links
def main(request):
    if request.method == "POST":
        link = request.POST.get('link')
        password = request.POST.get('password')
        comment = request.POST.get('comment')
        one_time = request.POST.get('one_time')
        date_radio = request.POST.get('date-radio')
        
        # Convert one_time to boolean
        if one_time == "True":
            one_time = True
        elif one_time == "False":
            one_time = False
        
        pub_date = timezone.now()  # Set publication date to current time
        token = 0

        try:
            # Create a new shortened_link instance
            shortener = shortened_link(pure_link=link, pub_date=pub_date, one_time=one_time)
            
            # Set expiration date if provided
            if date_radio == 'True':
                input_date = request.POST.get('date')
                naive_expire_date = datetime.strptime(input_date, '%Y-%m-%d').date()
                expire_date = timezone.make_aware(datetime.combine(naive_expire_date, datetime.min.time()), timezone.get_current_timezone())
                shortener.expire_date = expire_date
            
            # Set comment if provided
            if comment != "":
                shortener.comment = comment
            
            # Set password if provided
            if password != "":
                shortener.password = password
            
            # Generate and assign a unique token
            token = createToken()
            shortener.shortened_link = token
            
            # Save the new shortened link
            shortener.save()
            
            # Redirect to success view
            return redirect('index:success_view', token=token)
        except:
            raise Http404("Some error occurred!")  # Handle errors

    return render(request, "index/index.html")
