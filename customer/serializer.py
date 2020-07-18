from rest_framework import serializers
from customer.models import AccountDetails, AccountTransaction
import random
from django.core.mail import EmailMessage
from threading import Thread


def send_mail(transaction_type: str, status: str, amount: int, email_address: str, account_number: int):
    try:
        body = f"""A transaction of {0} have been made is {1} from your account{2} 
                   of amount {3}""".format(transaction_type, status, str(account_number)[-4:], amount)
        email = EmailMessage('Trasaction Alert', body, to=[email_address])
        email.send()
    except Exception as e:
        print(e)


def account_update(transaction: AccountTransaction):
    # transaction_type 0 is debit
    if transaction.transaction_type == 0:
        if transaction.account.balance < transaction.amount:
            transaction.status = 1
        else:
            transaction.account.balance -= transaction.amount
    elif transaction.transaction_type == 1:
        transaction.account.balance += transaction.amount
    transaction.account.save()
    transaction.save()
    return


class AccountDetailsSerializer(serializers.ModelSerializer):
    def create(self, validation_data):
        account_obj = AccountDetails.objects.create(**validation_data)
        return account_obj

    class Meta:
        model = AccountDetails
        fields = '__all__'


class AccountTransactionSerializer(serializers.ModelSerializer):
    # serializers.IntegerField
    account = serializers.IntegerField(source='account.account_number')
    status = serializers.CharField(source='get_status_display')
    transaction_type = serializers.CharField(source='get_transaction_type_display')

    class Meta:
        model = AccountTransaction
        fields = '__all__'


class CreateAccountTransactionSerializer(serializers.ModelSerializer):

    def create(self, validation_data):
        account = validation_data['account']
        account_query_set = AccountDetails.objects.filter(account_number=account.account_number)
        if account_query_set.exists():
            transaction = AccountTransaction.objects.create(**validation_data)
            account_update(transaction)
            Thread(target=send_mail, args=(transaction.transaction_type, transaction.status, transaction.amount,
                                           transaction.account.email_address,
                                           transaction.account.account_number,)).start()
            return transaction
        else:
            return False

    class Meta:
        model = AccountTransaction
        fields = '__all__'
