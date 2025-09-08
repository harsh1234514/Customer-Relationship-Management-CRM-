from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('prospect', 'Prospect'),
        ('partner', 'Partner'),
        ('vendor', 'Vendor'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='prospect')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Deal(models.Model):
    STAGE_CHOICES = [
        ('new', 'New'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='deals')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    probability = models.IntegerField(default=0, help_text="Probability of closing (0-100)")
    expected_close_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    @property
    def weighted_amount(self):
        return self.amount * (self.probability / 100)


class Activity(models.Model):
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('task', 'Task'),
        ('note', 'Note'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.title} - {self.activity_type}"

    def mark_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('email_campaign', 'Email Campaign'),
        ('trade_show', 'Trade Show'),
        ('cold_call', 'Cold Call'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Leads"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name or 'No Company'}"



class Task(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey('Deal', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ['-due_date']

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

