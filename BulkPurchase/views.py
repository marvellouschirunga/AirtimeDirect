from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import AirtimeRequest, User
from .forms import AirtimeRequestForm, UserForm, MyUserCreationForm
from django.utils import timezone
from .tasks import generate_csv_and_send_email

  
# Imports for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


# Create your views here.
def index(request):
    return HttpResponse('Hello, world. You are at the BulkAirtime index.')

def loginPage(request):
    #Handles user login functionality.
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user.is_online = True  # Mark user as online
            user.last_login = timezone.now()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    #Logs the user out and redirects to the homepage.
    user = request.user
    if user.is_authenticated:
        user.is_online = False  # Mark user as offline
        user.save()
    logout(request)
    return redirect('home')

def registerPage(request):
    # Handles user registration and email activation link generation.
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must activate via email
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def activateEmail(request, user, to_email):
    """Sends an email to the user with an account activation link."""
    mail_subject = 'Activate your PeerMentor.io user account.'
    message = render_to_string('base/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Please check your email {to_email} to activate your account.')
    else:
        messages.error(request, f'Problem sending email to {to_email}. Please check if the email is correct.')

def activate(request, uidb64, token):
    """Handles email account activation via the activation link."""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect('loginPage')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


# -------------------------
# CORE APPLICATION VIEWS
# -------------------------

def airtime_request_view(request):
    if request.method == 'POST':
        form = AirtimeRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The job has been sent for processing.')
            return redirect('success_page')
    else:
        form = AirtimeRequestForm()
    return render(request, 'airtime_request.html', {'form': form})              

def schedule_task_view(request):
    # Schedule the task to run at the specified time
    generate_csv_and_send_email.apply_async(eta=scheduled_time)
    messages.success(request, 'Batch job scheduled successfully.')
    return redirect('success_page')                                                                                                                                                                                                                                                           