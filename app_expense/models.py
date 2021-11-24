from django.db import models
from django.contrib.auth.models import User


class ExpenseType(models.TextChoices):
    GROUP = 'Group', 'Group'
    FRIEND = 'Friend', 'Friend'
    SETTLED_UP = 'SETTLED_UP', 'SETTLED_UP'


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_payer')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_payee')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_created_by', null=True, blank=True)
    amount = models.IntegerField()
    message = models.CharField(null=True, blank=True, max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    expense_type = models.CharField(choices=ExpenseType.choices, default=ExpenseType.FRIEND, max_length=128)

    def __str__(self) -> str:
        return f'[{self.expense_type}] {self.payer} > {self.payee} = {self.amount} '
