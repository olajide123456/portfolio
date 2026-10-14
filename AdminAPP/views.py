from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User, auth
from .mixins import CustomLoginRequiredMixin
from django.contrib import messages
from django.contrib import messages as django_messages
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from portfolioAPP.models import Contact
from django.urls import reverse_lazy
from .models import Project ,Experience ,Skill ,Signup
from django.views.generic import(ListView, DetailView, CreateView, DeleteView, UpdateView)




class dashboardListView(CustomLoginRequiredMixin, ListView):
    
    model = Project
    template_name = 'AdminAPP/dashboard.html'
    context_object_name = 'newproject'
    def get_context_data(self):
        context = super().get_context_data()
        # Dashboard counts
        context['total'] = Project.objects.count()
        context['experience'] = Experience.objects.count()
        context['message'] = Contact.objects.count()
        context['skill'] = Skill.objects.count()

        return context
  
#==========================
    # PROJECTS VIEWS
#==========================
class ProjectsListView(CustomLoginRequiredMixin, ListView):
    model = Project
    template_name = 'AdminAPP/projects.html'
    context_object_name = 'newproject'
    ordering = ['-id']
    paginate_by = 2
    def get_context_data(self):
        context = super().get_context_data()
        # Dashboard counts
        context['total'] = Project.objects.count()
        context['published_count'] = Project.objects.filter(status='published').count()
        context['draft'] = Project.objects.filter( status='draft').count()
        return context
   
class ProjectUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'AdminAPP/project_edit.html'
    fields = [ 'title','description','category','technologies','image',]
    success_url = reverse_lazy('AdminAPP:projects') 
    def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success(self.request,'Project updated successfully!' )
        return response

class ProjectDetailView(CustomLoginRequiredMixin, DetailView):
    model = Project
    template_name = 'AdminAPP/project_detail.html'
    context_object_name = 'project'

class ProjectDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'AdminAPP/project_del.html'
    success_url = reverse_lazy('AdminAPP:projects')
    def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success(self.request,'Project deleted successfully!'
        )
        return response
#==========================
    # PROJECTS VIEWS END
#==========================

#==========================
    #EXPERIENCE VIEWS 
#==========================

class ExperiencesListView(CustomLoginRequiredMixin, ListView):
    model = Experience
    template_name = 'AdminAPP/experiences.html'
    context_object_name = 'newexperience'
    ordering = ['-id']
    paginate_by = 2
  

class ExperienceDetailView(CustomLoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'AdminAPP/experience_detail.html'
    context_object_name = 'experience'

class ExperienceUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Experience
    template_name = 'AdminAPP/experience_edit.html'
    fields = ['title', 'company', 'start_date', 'end_date', 'description', 'technologies', 'employment_status']
    success_url = reverse_lazy('AdminAPP:experiences')
    def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success(self.request,'Experience updated successfully!')
        return response

class ExperienceDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'AdminAPP/experience_del.html'
    success_url = reverse_lazy('AdminAPP:experiences')  
    def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success(self.request,'Experience delete successfully!' )
        return response  
#==========================
    # EXPERIENCE VIEWS END
#==========================

class SkillsListView(CustomLoginRequiredMixin, ListView):
    model = Skill
    template_name = 'AdminAPP/skills.html'
    context_object_name = 'newskill'
    ordering = ['-id']
    paginate_by = 2 
    def get_context_data(self):
        context = super().get_context_data()
        context['total'] = Skill.objects.count()
        context['backend'] = Skill.objects.filter(category='Backend Development').count()
        context['frontend'] = Skill.objects.filter( category='Frontend Development').count()
        context['database'] = Skill.objects.filter( category='Database').count()
        return context 

class SkillUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Skill
    template_name = 'AdminAPP/skill_edit.html'
    fields = ['name', 'category', 'proficiency', 'display_order', 'icon', 'description', 'status']
    success_url = reverse_lazy('AdminAPP:skills')
       
    def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success( self.request,'Skill updated successfully!')
        return response   

class SkillDeleteView(CustomLoginRequiredMixin, DeleteView): 
     model = Skill
     template_name = 'AdminAPP/skill_del.html'
     success_url = reverse_lazy('AdminAPP:skills')  
     def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success(self.request,'Skill deleted successfully!')
        return response 
        # ==================================
        # Skill End
        # ==================================
            
class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Signup
    template_name = 'AdminAPP/profile.html'
    context_object_name = 'signup'
    fields = ['username','fullname','email','phone','title','location','bio','pic']
    def get_object(self, queryset=None):
        user_id = self.request.session.get('user_id')
        if not user_id:
            return redirect('AdminAPP:login')
        return Signup.objects.get(id=user_id)
    def get_success_url(self):
        return reverse_lazy('AdminAPP:profile')

class MessageListView(CustomLoginRequiredMixin, ListView):
    model = Contact
    template_name = 'AdminAPP/messages.html'
    context_object_name = 'newcontact'
    ordering = ['-id']
    paginate_by = 6

class MessageDetailView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        message = get_object_or_404(Contact, pk=pk)
        # Mark message as read when admin opens it
        if not message.is_read:
            message.is_read = True
            message.save(update_fields=['is_read'])
        return render(
            request,
            'AdminAPP/view_message.html',
            {'object': message}
        )
    def post(self, request, pk):
        message = get_object_or_404(Contact, pk=pk)
        reply_text = request.POST.get('reply', '').strip()
        if not reply_text:
            django_messages.error(
                request,
                'Please enter a reply before sending.'
            )
            return render(
                request,
                'AdminAPP/view_message.html',
                {'object': message}
            )
        try:
            send_mail(
                subject='Re: ' + message.subject,
                message=reply_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[message.email],
                fail_silently=False,
            )
            django_messages.success(
                request,
                'Reply sent to ' + message.email
            )
        except Exception as e:
            django_messages.error(
                request,
                'The reply could not be sent.'
            )
            print("REPLY EMAIL ERROR:", type(e).__name__)
            print(str(e))
        return render(
            request,
            'AdminAPP/view_message.html',
            {
                'object': message,
                'sent': True
            }
        )

class MarkMessageReadView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        if not request.session.get('user_id'):
            return redirect('AdminAPP:login')
        contact = get_object_or_404(Contact, pk=pk)
        contact.is_read = True
        contact.save(update_fields=['is_read'])
        django_messages.success(request,'Message marked as read successfully.')
        return redirect('AdminAPP:messages')


class MessageDeleteView(CustomLoginRequiredMixin, DeleteView): 
     model = Contact
     template_name = 'AdminAPP/message_del.html'
     success_url = reverse_lazy('AdminAPP:messages')  
     def form_valid(self, form):
        response = super().form_valid(form)
        django_messages.success( self.request,'message deleted successfully!' )
        return response 

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')
    

def add_projects(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        status = request.POST['status']
        technologies = request.POST['technologies']
        project_url = request.POST['live_demo']
        github_url = request.POST['github_repo']
        image = request.FILES.get('image')
        Project.objects.create(
            title=title,
            description=description,
            category=category,
            status=status,
            technologies=technologies,
            project_url=project_url,
            github_url=github_url,
            image=image
        )
       
        django_messages.info(
            request,
            'Project Successfully Created'
        )
        return redirect('AdminAPP:projects')
    return render(request,'AdminAPP/add_projects.html'
    )


def add_experiences(request):
    if request.method == 'POST':
        title = request.POST['title']
        company = request.POST['company']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        employment_status = request.POST['employment_status']
        description = request.POST['description']
        responsibilities = request.POST.getlist('responsibilities')
        technologies = request.POST['technologies']
        visibility = request.POST['visibility']
        display_order = request.POST['display_order']
        if start_date:
            start_date = start_date + '-01'
        if end_date:
            end_date = end_date + '-01'
        else:
            end_date = None
        responsibilities = ', '.join(
            responsibility.strip()
            for responsibility in responsibilities
            if responsibility.strip()
        )
        Experience.objects.create(title=title,company=company,start_date=start_date,end_date=end_date,employment_status=employment_status,description=description,responsibilities=responsibilities,technologies=technologies,visibility=visibility,display_order=display_order)
        django_messages.info(request,'Experience Successfully Created')
        return redirect('AdminAPP:experiences')

    return render(request,'AdminAPP/add_experiences.html'
    )


def add_skills(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        proficiency = request.POST['proficiency']
        display_order = request.POST['display_order']
        icon = request.POST['icon']
        description = request.POST['description']
        status = request.POST['status']
         # If display order is empty, use 1
        if not display_order:
            display_order = 1
        else:
            display_order = int(display_order)
        # If proficiency is empty, use 80
        if not proficiency:
            proficiency = 80
        else:
            proficiency = int(proficiency)
        Skill.objects.create(name=name,category=category,proficiency=proficiency,display_order=display_order, icon=icon, description=description, status=status )
        django_messages.success( request,'Skill Successfully Created')
        return redirect('AdminAPP:skills')
    return render(
        request,
        'AdminAPP/add_skills.html'
    )    




class CustomLoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('AdminAPP:login')

        response = super().dispatch(request, *args, **kwargs)

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response


        