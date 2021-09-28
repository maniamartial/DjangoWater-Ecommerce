
from payments.form import PhoneNumber
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword


def getAccessToken(request):
    consumer_key = 'XjWEg9z1ihL9zoXO1JRaCOhfIJAgB8cu'
    consumer_secret = 'y48BAeDDA0AgXqI2'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def showform(request):
    form = PhoneNumber()
    if request.method == 'POST':
        form = PhoneNumber(request.POST)
        if form.is_valid():

            form.save()
            number = '254' + str(form.cleaned_data.get('phone'))
            print(number)
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": 50,
                "PartyA":  number,  # replace with your phone number to get stk push -600989
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": number,  # replace with your phone number to get stk push
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Mania",
                "TransactionDesc": "Fear not for I am with you"
            }

            response = requests.post(api_url, json=request, headers=headers)
            print(response)
            return HttpResponse('success')
           # return redirect('waters')

    context = {'form': form}
    return render(request, 'payments/payments.html', context)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254768534225,  # replace with your phone number to get stk push -600989
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254768534225,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Mania",
        "TransactionDesc": "Fear not for I am with you"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return HttpResponse('success')
