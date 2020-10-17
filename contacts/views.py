from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        contact = Contact(listing=listing, listing_id=listing_id, email=email, name=name, phone=phone,
                          message=message, realtor_email=realtor_email, user_id=user_id)

        contact.save()

        messages.success(request, 'Your request has been submitted, a realtor will get back to You soon')

        return redirect('/listings/' + listing_id)

