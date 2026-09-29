from django.db import models
from django.contrib.auth.models import User


class Lead(models.Model):

    LEAD_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]

    LEAD_SOURCE = [
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('referral', 'Referral'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True)

    company = models.CharField(max_length=200, blank=True)

    job_title = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20,
        choices=LEAD_STATUS,
        default='new'
    )

    source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE,
        default='website'
    )

    score = models.IntegerField(default=0)

    notes = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_leads'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    converted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']


class Activity(models.Model):

    ACTIVITY_TYPES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('task', 'Task'),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES
    )

    subject = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    due_date = models.DateTimeField(
        null=True,
        blank=True
    )

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Activities"


class LeadScoreRule(models.Model):

    name = models.CharField(max_length=100)

    field = models.CharField(max_length=50)

    operator = models.CharField(max_length=20)

    value = models.CharField(max_length=100)

    points = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-points']


class PipelineStage(models.Model):

    name = models.CharField(max_length=100)

    order = models.IntegerField()

    description = models.TextField(blank=True)

    color = models.CharField(
        max_length=7,
        default='#7C4DFF'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class ConversionRate(models.Model):

    date = models.DateField()

    total_leads = models.IntegerField(default=0)

    converted_leads = models.IntegerField(default=0)

    conversion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['date'],
                name='unique_conversion_date'
            )
        ]