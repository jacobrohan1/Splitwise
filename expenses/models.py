from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this line

    def __str__(self):
        return self.name


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])

    def __str__(self):
        return self.description

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.participant.name} - {self.share}"
