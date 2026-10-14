from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User, auth
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.views import View
from datetime import date
from django.views.generic import TemplateView
from AdminAPP.models import Project ,Experience ,Skill ,Signup

import secrets
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import Contact
from portfolioAPP.services.gemini_reply import generate_ai_reply


def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'services.html')   
def contact(request):
    return render(request, 'contact.html')




class IndexListView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self):
        context = super().get_context_data()
        # =========================
        # PROFILE
        # =========================
        context['profile'] = Signup.objects.order_by('id').first()
        # =========================
        # PROJECTS
        # =========================
        projects = Project.objects.filter(
            status='published'
        ).order_by(
            'display_order',
            '-created_at'
        )
        context['projects'] = projects[:4]
        context['project_count'] = projects.count()

        # =========================
        # TECHNOLOGIES
        # =========================
        technologies = []

       
        context['technologies'] = technologies
        context['technology_count'] = len(technologies)

        # =========================
        # EXPERIENCE
        # =========================
        experiences = Experience.objects.filter(
            visibility='published'
        ).order_by(
            'display_order',
            '-start_date'
        )
        context['experiences'] = experiences
        context['experience_count'] = experiences.count()

        # =========================
        # YEARS OF EXPERIENCE
        # =========================
        first_experience = experiences.order_by(
            'start_date'
        ).first()
        if first_experience:
            today = date.today()
            years = (
                today.year -
                first_experience.start_date.year
            )
            if (today.month, today.day) < (
                first_experience.start_date.month,
                first_experience.start_date.day
            ):
                years -= 1
            context['years_experience'] = max(years, 0)
        else:
            context['years_experience'] = 0
        return context


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if Signup.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exist')
                return redirect('signup')
            elif Signup.objects.filter(username=username).exists():
                messages.info(request, 'Username has been Used ')
                return redirect('signup')    
            else:
                Signup.objects.create(username=username,fullname=fullname,email=email, password=password)
                # signup.save()
                messages.info(request, 'User Successfully Created')
                return redirect('signup')    
        else:
            messages.info(request, 'Password not Matching')
            return redirect('signup')
    else:            
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Signup.objects.get(email=email, password=password)
            request.session['user_id']= user.id
            return redirect('/add/')
        except Signup.DoesNotExist:
            messages.error(request,'invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')      


class ProjectsListView(ListView):
    model = Project
    template_name = 'projects.html'
    context_object_name = 'newproject'

class ExperiencesListView(ListView):
    model = Experience
    template_name = 'experience.html'
    context_object_name = 'newexperience'    

class SkillsListView(ListView):
    model = Skill
    template_name = 'skills.html'
    context_object_name = 'newskill'
    ordering = ['category', 'display_order', '-id']




def contact(request):
    # Creates the contact function and receives the visitor's request.
    if request.method == 'POST':
        contact_message = Contact.objects.create(
          # Creates a new Contact record and saves it in the database.
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),# 
            service=request.POST.get('service'),
            budget=request.POST.get('budget'),
            timeline=request.POST.get('timeline'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        try: # Starts a block where Django will try to perform the following operations.
            ai_reply = generate_ai_reply(contact_message)# Sends the client's information to Gemini and generates an AI reply.
            contact_message.ai_reply = ai_reply
            # Stores the AI-generated reply inside the Contact object.
            contact_message.save(update_fields=['ai_reply']) # Saves only the AI reply into the database.
            send_mail(# Starts sending an email to the client.
                'Re: ' + contact_message.subject,# Creates the email subject using the client's subject.
                ai_reply, # Uses the AI-generated reply as the email message.
                settings.DEFAULT_FROM_EMAIL, # Uses your configured email address as the sender.
                [contact_message.email] # Sends the email to the client's email address.
            )
            send_mail( # Starts sending a second email to you.
                'New Portfolio Enquiry: ' + contact_message.subject, # Creates the subject for your notification email.
                f"""
Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone}
Service: {contact_message.service}
Budget: {contact_message.budget}
Timeline: {contact_message.timeline}
Message: {contact_message.message}
""",
                settings.DEFAULT_FROM_EMAIL,# Uses your email address as the sender.
                [settings.DEFAULT_FROM_EMAIL] # Sends the notification to your own email address.
            )
            messages.success(request, 'Successfully sent!')
        except Exception as e:
            print("ERROR:", e)
            messages.error(request, 'Something went wrong.')
        return redirect('contact')
    return render(request, 'contact.html')
   




class ForgotPasswordView(View): # Creates a class-based view for handling forgotten passwords.
    def get(self, request): # Runs when the user opens the forgot-password page.
        return render(request, 'forgot-password.html') # Displays the forgot-password form.
    def post(self, request): # Runs when the user submits their email.
        try:# Tries to find the user's account.
            user = Signup.objects.get(email=request.POST.get('email'))
            user.reset_token = secrets.token_urlsafe(32) 
            user.reset_token_created = timezone.now() 
            user.save() # Saves the token and creation time to the database.
            link = request.build_absolute_uri(
                f'/reset-password/{user.reset_token}/'
            ) # Creates the complete password-reset link.
            send_mail(
                'Reset Your Password',
                f'Reset your password here:{link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            ) # Sends the reset link to the user's email.

    
        except Signup.DoesNotExist: # Runs if no account exists with that email.
             return render(request, 'forgot-password.html', {
            'error': 'Email does not exist.'
        })
        return redirect('login')
        # Sends the user back to the login page.   

class ResetPasswordView(View):
    def get(self, request, token):
        # Show the reset password page.
        return render(request, 'reset-password.html')
    def post(self, request, token):
        # Find the user with this reset token.
        try:
            user = Signup.objects.get(reset_token=token)
        except Signup.DoesNotExist:
            return render(request, 'reset-password.html', {
                'error': 'Invalid or expired reset link.'
            })

        # Get the new passwords.
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        # Check that both passwords match.
        if password != confirm:
            return render(request, 'reset-password.html', {
                'error': 'Passwords do not match.'
            })

        # Save the new password and remove the token.
        user.password = password
        user.reset_token = None
        user.reset_token_created = None
        user.save()

        # Return to login.
        return redirect('login')