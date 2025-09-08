from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Company, Contact, Lead, Deal, Activity
from .forms import CompanyForm, ContactForm, LeadForm, DealForm, ActivityForm
from .utils.email_utils import send_activity_email


# ----------------- Authentication -----------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'crm/login.html', {'error': 'Invalid username or password'})
    return render(request, 'crm/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# ----------------- Dashboard -----------------
@login_required
def dashboard(request):
    companies_count = Company.objects.count()
    if request.user.is_superuser:
        contacts_count = Contact.objects.count()
        leads_count = Lead.objects.count()
        deals_count = Deal.objects.count()
        recent_activities = Activity.objects.order_by('-created_at')[:5]
        upcoming_activities = Activity.objects.filter(due_date__gte=timezone.now()).order_by('due_date')[:5]
    else:
        contacts_count = Contact.objects.filter(assigned_to=request.user).count()
        leads_count = Lead.objects.filter(assigned_to=request.user).count()
        deals_count = Deal.objects.filter(assigned_to=request.user).count()
        recent_activities = Activity.objects.filter(assigned_to=request.user).order_by('-created_at')[:5]
        upcoming_activities = Activity.objects.filter(assigned_to=request.user, due_date__gte=timezone.now()).order_by('due_date')[:5]

    total_pipeline_value = sum([d.amount for d in Deal.objects.all()])
    won_deals = Deal.objects.filter(stage='won').count()
    lead_conversion_rate = round((won_deals / leads_count * 100) if leads_count else 0, 2)

    context = {
        'companies_count': companies_count,
        'contacts_count': contacts_count,
        'leads_count': leads_count,
        'deals_count': deals_count,
        'recent_activities': recent_activities,
        'upcoming_activities': upcoming_activities,
        'total_pipeline_value': total_pipeline_value,
        'won_deals': won_deals,
        'lead_conversion_rate': lead_conversion_rate,
    }
    return render(request, 'crm/dashboard.html', context)

# ----------------- Helper -----------------
def is_admin(user):
    return user.is_superuser

# ----------------- Company Views -----------------
@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'crm/company_list.html', {'companies': companies})

@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'crm/company_form.html', {'form': form})

@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'crm/company_form.html', {'form': form})

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'crm/company_detail.html', {'company': company})

@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.user.is_superuser:
        company.delete()
    return redirect('company_list')


# ----------------- Contact Views -----------------
@login_required
def contact_list(request):
    if is_admin(request.user):
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(assigned_to=request.user)
    return render(request, 'crm/contact_list.html', {'contacts': contacts})

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.assigned_to = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'crm/contact_form.html', {'form': form})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'crm/contact_detail.html', {'contact': contact})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'crm/contact_form.html', {'form': form})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.user.is_superuser or contact.assigned_to == request.user:
        contact.delete()
    return redirect('contact_list')

# ----------------- Lead Views -----------------
@login_required
def lead_list(request):
    if is_admin(request.user):
        leads = Lead.objects.all()
    else:
        leads = Lead.objects.filter(assigned_to=request.user)
    return render(request, 'crm/lead_list.html', {'leads': leads})

@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.assigned_to = request.user
            lead.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'crm/lead_form.html', {'form': form})

@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'crm/lead_form.html', {'form': form})

@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'crm/lead_detail.html', {'lead': lead})


@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.user.is_superuser or lead.assigned_to == request.user:
        lead.delete()
    return redirect('lead_list')

# ----------------- Deal Views -----------------
@login_required
def deal_list(request):
    if is_admin(request.user):
        deals = Deal.objects.all()
    else:
        deals = Deal.objects.filter(assigned_to=request.user)
    return render(request, 'crm/deal_list.html', {'deals': deals})

@login_required
def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.assigned_to = request.user
            deal.save()
            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request, 'crm/deal_form.html', {'form': form})

@login_required
def deal_edit(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            return redirect('deal_list')
    else:
        form = DealForm(instance=deal)
    return render(request, 'crm/deal_form.html', {'form': form})

@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    return render(request, 'crm/deal_detail.html', {'deal': deal})


@login_required
def deal_delete(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.user.is_superuser or deal.assigned_to == request.user:
        deal.delete()
    return redirect('deal_list')

# ----------------- Activity Views -----------------
@login_required
def activity_list(request):
    if is_admin(request.user):
        activities = Activity.objects.all()
    else:
        activities = Activity.objects.filter(assigned_to=request.user)

    return render(request, 'crm/activity_list.html', {'activities': activities})

@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.assigned_to = request.user
            activity.save()
            
#-------------------------Email notification-----------------------
            # Send email notification to the assigned user
            if activity.assigned_to and activity.assigned_to.email:
                send_activity_email(
                    to_email=activity.assigned_to.email,
                    activity_title=activity.title,
                    activity_type=activity.activity_type,
                    due_date=activity.due_date,
                    created_by=request.user.username
                )
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'crm/activity_form.html', {'form': form})


@login_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'crm/activity_detail.html', {'activity': activity})


@login_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'crm/activity_form.html', {'form': form})

@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.is_superuser or activity.assigned_to == request.user:
        activity.delete()   
    return redirect('activity_list')

@login_required
def activity_complete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    
    # Only superuser or the assigned user can mark it complete
    if request.user.is_superuser or activity.assigned_to == request.user:
        activity.status = 'completed'
        activity.completed_at = timezone.now()
        activity.save()
    
    return redirect('activity_list')


