from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.views import APIView
from customer.serializer import AccountDetailsSerializer, AccountTransactionSerializer, \
    CreateAccountTransactionSerializer
from customer.models import AccountDetails, AccountTransaction
import random
import datetime
import pandas as pd
from django.http import HttpResponseRedirect


def get_account_number() -> int:
    account_number = int()
    loop_iterator = True
    while loop_iterator:
        account_number = random.randint(10000000, 99999999)
        account_query_set = AccountDetails.objects.filter(account_number=account_number)
        if not account_query_set.exists():
            loop_iterator = False
    return account_number


# Create your views here.
class FirstTrail(APIView):

    def post(self, request):
        output = {
            "data": [],
            "message": "everything is fine",
            "status": "success",
            "data_type": "list"
        }
        try:
            # add account number in the request data
            request.data['account_number'] = get_account_number()
            # get account details from db
            account_details = AccountDetailsSerializer(data=request.data)
            if account_details.is_valid(raise_exception=True):
                data = account_details.validated_data
                account_details.create(data)
                output['data'] = account_details.data
                return JsonResponse(output)
            else:
                output['status'] = 'error'
                output['message'] = account_details.errors
                return JsonResponse(output, status=404)
        except Exception as e:
            print(e)
            output['status'] = 'error'
            output['message'] = 'error encountered'
            return JsonResponse(output, status=500)


# Debit and credit
class SecondTrail(APIView):
    def post(self, request):
        output = {
            "data": [],
            "message": "everything is fine",
            "status": "success",
            "data_type": "list"
        }
        try:
            # add start date in request data
            request.data['start_date'] = datetime.datetime.now()

            account_transaction = CreateAccountTransactionSerializer(data=request.data)
            if account_transaction.is_valid():
                data = account_transaction.validated_data
                transaction = account_transaction.create(data)
                output['data'] = AccountTransactionSerializer(transaction).data
                return JsonResponse(output)
            else:
                output['status'] = 'error'
                output['message'] = account_transaction.errors
                return JsonResponse(output, status=400)
        except Exception as e:
            print(e)
            output['status'] = 'error'
            output['message'] = 'error encountered'
            return JsonResponse(output, status=500)


# Account Enquiry
class ThirdTrail(APIView):
    def get(self, request, account_number):
        output = {
            "data": {},
            "message": "everything is fine",
            "status": "success",
            "data_type": "dict"
        }
        try:
            # get account number information
            account_details_obj = AccountDetails.objects.filter(account_number=account_number)
            if account_details_obj.exists():
                account_details_serializer_obj = AccountDetailsSerializer(account_details_obj[0])
                output['data']['account_details'] = account_details_serializer_obj.data
                # get transaction details from db
                account_transaction_obj = AccountTransaction.objects.filter(account__account_number=account_number)
                if account_transaction_obj.exists():
                    account_details_serializer_obj = AccountTransactionSerializer(account_transaction_obj, many=True)
                    output['data']['account_transaction'] = account_details_serializer_obj.data
                return JsonResponse(output)
            else:
                output['status'] = 'error'
                output['message'] = 'account number not found'
                return JsonResponse(output, status=404)
        except Exception as e:
            print(e)
            output['status'] = 'error'
            output['message'] = 'error encountered'
            return JsonResponse(output, status=500)


# download file for manager
class FourthTrail(APIView):
    def post(self, request):
        output = {
            "message": "everything is fine",
            "status": "success"
        }
        try:
            # specifying date format for the reference
            date_format = '%Y-%m-%d %H:%M:%S'

            # gathering data from request
            from_date = request.data['from_date']
            to_date = request.data['to_date']
            account_numbers = request.data['account_number']

            # convert string to datetime object
            from_date = datetime.datetime.strptime(from_date, date_format)

            # convert string to datetime object
            to_date = datetime.datetime.strptime(to_date, date_format)
            # get transaction details from db
            account_transaction_obj = AccountTransaction.objects.filter(
                account__account_number__in=account_numbers).filter(start_date__lte=to_date).filter(
                start_date__gte=from_date)
            if account_transaction_obj.exists():
                account_transaction_serializer_obj = AccountTransactionSerializer(account_transaction_obj, many=True)
                # converting serialized data to dataframe
                df = pd.DataFrame(account_transaction_serializer_obj.data)

                # removing id column
                df.drop(columns=['id'], inplace=True)

                # saving file in media folder
                df.to_excel('media/export_excel.xlsx', index=False)
                # generating downloadable url for the excel file
                output['url'] = request.build_absolute_uri('/media/export_excel.xlsx')
                return JsonResponse(output)
            else:
                output['status'] = 'error'
                output['message'] = 'no record found'
                return JsonResponse(output, status=404)
        except Exception as e:
            print(e)
            output['status'] = 'error'
            output['message'] = 'error encountered'
            return JsonResponse(output, status=500)
