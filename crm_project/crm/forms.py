from django import forms
from django.contrib.auth.models import User
from .models import Company, Contact, Deal, Activity, Lead

# --- Company Form ---
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'website', 'phone', 'email', 'address', 'city', 'state', 'country', 'postal_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'company@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        }

# --- Contact Form ---
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'job_title', 'company', 
                  'contact_type', 'address', 'city', 'state', 'country', 'postal_code', 'notes', 'assigned_to']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'contact_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes...'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.all().order_by('name')
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        self.fields['assigned_to'].required = False

# --- Deal Form ---

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['title','contact','company','amount','stage','priority','probability','expected_close_date','assigned_to']
        widgets = {
        'title': forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Deal Title'}),
        'contact': forms.Select(attrs={'class':'form-control'}),
        'company': forms.Select(attrs={'class':'form-control'}),
        'amount': forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Deal Amount'}),
        'stage': forms.Select(attrs={'class':'form-control'}),
        'priority': forms.Select(attrs={'class':'form-control'}),
        'probability': forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Probability %'}),
        'expected_close_date': forms.DateInput(attrs={'class':'form-control' , 'type':'date'}),
        'assigned_to': forms.Select(attrs={'class':'form-control'}),    
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contact.objects.select_related('company').order_by('last_name', 'first_name')
        self.fields['company'].queryset = Company.objects.all().order_by('name')
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        self.fields['assigned_to'].required = False

# --- Activity Form ---
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'activity_type', 'status', 'description', 'contact', 'deal', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity Title'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Activity description...'}),
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'deal': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contact.objects.select_related('company').order_by('last_name', 'first_name')
        self.fields['deal'].queryset = Deal.objects.select_related('company').order_by('title')
        self.fields['contact'].required = False
        self.fields['deal'].required = False
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.fields['assigned_to'].required = False

# --- Lead Form ---
class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone', 'company_name', 'status', 'assigned_to']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.fields['assigned_to'].required = False
