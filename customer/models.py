from django.db import models


# Create your models here.
# You need to design a banking system with following minimum specifications -
#
# A bank system which manages users’ account information. A customer of this bank can invoke the following operations
# 1. deposit (this operation increases the balance of user account by a given amt)
# 2. withdraw (this operation decreases the balance of user account by given amt)
# 3. enquiry ( this operation returns the balance of user account etc)
# 4. customer should receive emails on transactions
# 5. the bank manager should be able to download excel of transaction histories for a specific time period for individual/a collection of customers
class AccountDetails(models.Model):
    fullname = models.CharField(max_length=20, null=False, blank=False)
    account_number = models.BigIntegerField(null=False, primary_key=True)
    address = models.TextField(null=False, blank=False)
    balance = models.BigIntegerField(null=False, blank=False)
    email_address = models.EmailField(max_length=254, blank=False, null=False)


class AccountTransaction(models.Model):
    transaction_choice = (
        (0, 'debit'),
        (1, 'credit'),
    )
    status_choice = (
        (0, 'accepted'),
        (1, 'declined'),
    )
    account = models.ForeignKey(AccountDetails, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=False, blank=False)
    amount = models.BigIntegerField(null=False, blank=False)
    transaction_type = models.IntegerField(choices=transaction_choice, default=0)
    status = models.IntegerField(choices=status_choice, default=0)
