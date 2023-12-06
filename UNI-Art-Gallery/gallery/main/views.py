from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from .models import User_Credentials, Art, Art_Tags, User_Info, User_Social
from .forms import LoginForm, ArtForm, RegisterUserForm, Tag_Search, UserCredentialsForm,UserInfoForm,UserSocialForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse

import uuid


def landing(request):
    return render(request, "landing.html")


@login_required(login_url="/login")
def main(request):
    if request.method == 'POST':
        Search = Tag_Search(request.POST)
        if Search.is_valid():
            Tag1 = Search.cleaned_data['Tag1']
            Tag2 = Search.cleaned_data['Tag2']
            Tag3 = Search.cleaned_data['Tag3']
            
            Results = Art_Tags.objects.all()
            if Tag1:
                Results = Results.filter(Tag1=Tag1)
            if Tag2:
                Results = Results.filter(Tag2=Tag2)
            if Tag3:
                Results = Results.filter(Tag3=Tag3)

            Search = Tag_Search()
            username = request.user.username

            context = {
            "username": username,
            "pictures": Results,
            "form": Search,
            }
            return render(request, "main_screen.html",context)

        else:
            return HttpResponse(Search.errors.as_json())
    
    else:
        Search = Tag_Search()
        username = request.user.username
        pictures = Art_Tags.objects.all()

        context = {
        "username": username,
        "pictures": pictures,
        "form": Search,
        }
        return render(request, "main_screen.html", context)
        

@csrf_protect
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                # Settings.py redirects to a specific URL
            else:
                print("No User")
                return HttpResponseRedirect(
                    "/"
                )  # Use return to actually perform the redirect
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


@login_required(login_url="/login")
@csrf_protect
def art_creation(request):
    username = request.user
    if request.method == "POST":
        # print(request.FILES.get('image'))
        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(user=username)
            return redirect("/login/main/creation")
        else:
            return HttpResponse(form.errors.as_json())
    else:
        form = ArtForm()
        user_id = request.user.id
        username = request.user.username
        own_creations = Art_Tags.objects.filter(arts_id__Owner_ID__id=user_id)

        return render(
            request,
            "creation.html",
            {"form": form, "username": username, "own_creations": own_creations},
        )


def register(request):
    if request.method == "POST":
        form1 = RegisterUserForm(request.POST)
        if form1.is_valid():
            try:
                form1.save()
                return redirect("/login")
            except:
                return HttpResponse(form1.errors.as_json())
        else:
            return HttpResponse(form1.errors.as_json())
    else:
        form1 = RegisterUserForm()
        return render(request, "register.html", {"form1": form1})


@login_required(login_url="/login")
def author(request):
    if request.method == "POST":
        username = request.user.username
        author = request.POST.get('author')

        Socials = User_Social.objects.filter(Social_Owner=author).first
        author_info = User_Info.objects.filter(User_ID=author).first
        Arts= Art_Tags.objects.filter(arts_id__Owner_ID__id=author)
        
        #return HttpResponse(author_info)
        return render(request, "author.html", {"Arts":Arts, 'username':username, "Info":author_info,'Social':Socials})
    else:
        return render(request, "author.html")


def account(request):
    user_id = request.user.id
    user_credentials = get_object_or_404(User_Credentials, id=user_id)
    user_info = user_credentials.info
    user_social = user_credentials.social

    if request.method == 'POST':
        credentials_form = UserCredentialsForm(request.POST, instance=user_credentials)
        info_form = UserInfoForm(request.POST, instance=user_info)
        social_form = UserSocialForm(request.POST, instance=user_social)

        if credentials_form.is_valid() and info_form.is_valid() and social_form.is_valid():
            credentials_form.save()
            info_form.save()
            social_form.save()
            return redirect('/login/main/')
    else:
        credentials_form = UserCredentialsForm(instance=user_credentials)
        info_form = UserInfoForm(instance=user_info)
        social_form = UserSocialForm(instance=user_social)

    return render(request, 'account.html', {
        'credentials_form': credentials_form,
        'info_form': info_form,
        'social_form': social_form,
    })







# PAYMENT TESTING
def deals_Creation(request):
    host = request.get_host()
    Payment_Info ={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '20.00',
        'item_name': 'Dibujo Isometrico',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url':f'http://{host}{reverse("paypal-ipn")}',
        'return_url':f'http://{host}{reverse("paypal-return")}',
        'cancel_return':f'http://{host}{reverse("paypal-cancel")}',


    }

    form = PayPalPaymentsForm(initial=Payment_Info)
    context = {'form': form}

  
    return render(request,'deal_creation.html', context)
   
    
def paypal_return(request):
    messages.success(request,"Has Donado Correctamente")
    return redirect("/login/main/new_deal")

def paypal_cancel(request):
    messages.success(request,"No Has podido Donar :(")
    return redirect("/login/main/new_deal")


