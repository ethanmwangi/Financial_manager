from django.db import models
from django.conf import settings   # ✅ use settings.AUTH_USER_MODEL

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('transport', 'Transport'),
    ('shopping', 'Shopping'),
    ('bills', 'Bills'),
    ('other', 'Other'),
]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return f"{self.title} - {self.transaction_type} - {self.amount}"
