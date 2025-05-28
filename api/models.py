from django.db import models
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORIES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('health', 'Health'),
        ('sales', 'Sales'),
        ('salary', 'Salary'),
        ('investment', 'Investment'),
        ('education', 'Education'),
        ('shopping', 'Shopping'),
        ('travel', 'Travel'),
        ('gifts', 'Gifts'),
        ('donations', 'Donations'),
        ('bills', 'Bills'),
        ('subscriptions', 'Subscriptions'),
        ('savings', 'Savings'),
        ('loans', 'Loans'),
        ('insurance', 'Insurance'),
        ('taxes', 'Taxes'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    category_other = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.transaction_type}) - {self.amount}"
    
class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    all_day = models.BooleanField(default=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='calendar_events', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Bill(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bills', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
    
class Sale(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sales', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
    
class PettyCash(models.Model):
    control_number = models.CharField(max_length=11, blank=True, unique=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    isApproved = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='petty_cash', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

def generate_unique_control_number():
    while True:
        code = f"PC-{uuid.uuid4().hex[:8].upper()}"
        if not PettyCash.objects.filter(control_number=code).exists():
            return code

@receiver(pre_save, sender=PettyCash)
def add_control_number(sender, instance, **kwargs):
    if not instance.control_number:
        instance.control_number = generate_unique_control_number()