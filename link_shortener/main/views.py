from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import shortened_link
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator

# Error message text
error_text = "An error occurred, try again later."

# Redirect to the main page
def main(request):
    return redirect("index:main")

# View function to display the shortened link details
def view_link(request, token):
    # Get the link object from the database using the token
    link_fetched = shortened_link.objects.get(shortened_link=token)

    # Check if the token is still valid
    if not link_fetched.is_valid:
        return render(request, "main/detail.html", {"token": token, "item": link_fetched, "is_valid": link_fetched.is_valid})
    
    # Check if the token is a one-time use token and if it has already been used
    one_time = link_fetched.one_time
    times_used = link_fetched.times_used
    if one_time and times_used >= 1:
        link_fetched.is_valid = False
        link_fetched.save()
        return render(request, "main/detail.html", {"token": token, "item": link_fetched, "is_valid": link_fetched.is_valid})

    # Check if the token has an expiration date and if it has expired
    if link_fetched.expire_date:
        today_date = timezone.now()
        expire_date = link_fetched.expire_date
        if expire_date < today_date:
            link_fetched.is_valid = False
            link_fetched.save()
            return render(request, "main/detail.html", {"token": token, "item": link_fetched, "is_valid": link_fetched.is_valid})

    # Handle POST request for password verification
    if request.method == "POST":
        password = request.POST.get('password')
        true_password = link_fetched.password
        if password == true_password:
            link_fetched.times_used += 1
            link_fetched.save()
            return HttpResponseRedirect(link_fetched.pure_link)
        else:
            messages.error(request, 'Wrong password!')

    try:
        # Redirect if there is no password, else render the detail page with password input
        if link_fetched.password == "":
            link_fetched.times_used += 1
            link_fetched.save()
            return HttpResponseRedirect(link_fetched.pure_link)
        else:
            return render(request, "main/detail.html", {"token": token, "item": link_fetched, "is_valid": link_fetched.is_valid})
    except shortened_link.DoesNotExist:
        raise Http404("Link does not exist!")

# Function to show the latest 10 shortened links
def showall(request):
    all_links_list = shortened_link.objects.order_by("-pub_date")
    paginator = Paginator(all_links_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "all_links_list": all_links_list,
        "page_obj": page_obj,
    }
    return HttpResponse(render(request, "main/showall.html/", context))

# Function to edit the details of a shortened link
def editlink(request, token):
    item = shortened_link.objects.get(shortened_link=token)
    
    # Handle different types of POST requests for editing the link
    if request.method == "POST":
        if request.POST.get("action") == "change_submit":
            # Change password functionality
            current_pass = request.POST.get("current-password")
            new_pass = request.POST.get("new-password")
            confirm_pass = request.POST.get("confirm-password")
            real_pass = item.password
            print(current_pass, new_pass, confirm_pass, real_pass)
            if real_pass == current_pass and new_pass == confirm_pass:
                if new_pass == "":
                    item.password = ""
                    item.save()
                    messages.success(request, "You deleted your password successfully.")
                else:
                    try:
                        item.password = new_pass
                        item.save()
                        messages.success(request, "You changed the password successfully.")
                    except:
                        messages.warning(request, error_text)  
            else:
                messages.warning(request, "Error, the given argument(s) are incorrect.")
        elif request.POST.get("action") == "delete":
            item.is_valid = False
            item.save()
            return redirect("index:main")

        elif request.POST.get("action") == "add_submit":
            # Add password functionality
            add_pass = request.POST.get("add-password")
            add_confirm_pass = request.POST.get("add-confirm-password")
            if add_pass == add_confirm_pass:
                try:
                    item.password = add_pass
                    item.save()
                    messages.success(request, "You assigned a password successfully.")
                except:
                    messages.warning(request, error_text)         
            else:
                messages.warning(request, "Error, passwords are not same.")
        elif request.POST.get("action") == "comment_submit":
            # Update comment functionality
            new_comment = request.POST.get("comment")
            if item.comment != new_comment:
                try:
                    item.comment = new_comment
                    item.save()
                    messages.success(request, "You updated your comment successfully.")
                except:
                    messages.warning(request, error_text)
        elif request.POST.get("action") == "update_date":
            # Update expiration date functionality
            input_date = request.POST.get('date')
            naive_expire_date = datetime.strptime(input_date, '%Y-%m-%d').date()
            new_date = timezone.make_aware(datetime.combine(naive_expire_date, datetime.min.time()), timezone.get_current_timezone())
            exp_date = item.expire_date
            if exp_date:
                if exp_date != new_date:
                    item.expire_date = new_date
                    item.save()
                    messages.success(request, "You updated your link's expiration date successfully.")
                if exp_date == new_date:
                    messages.warning(request, "The dates are the same!")
            else:
                item.expire_date = new_date
                item.save()
                messages.success(request, "You added a deadline to your link successfully.")
    
    # Prepare the context for rendering the edit page
    if item.password == "":
        password = None
    else: 
        password = item.password
    if item.comment:
        comment = item.comment
    else:
        comment = ""
    context = {
        "link": item.pure_link,
        'password': password,
        'comment': comment,
        'shortened_link': token,
        'times_used': item.times_used,
        'exp_date': item.expire_date,
    }
    return render(request, "main/edit.html/", context)
