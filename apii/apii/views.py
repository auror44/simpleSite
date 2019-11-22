from django.shortcuts import render
import pyrebase
import random
from django.http import HttpResponse

config = {
    ##Add your firebase config here

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
from .bankConn import BankProcess
bp = BankProcess()
c=0

def signIn(request):
    return render(request, 'signIn.html')


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    user = auth.sign_in_with_email_and_password(email, passw)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    api_token = bp.create_token()
    supported_banks = bp.supported_banks(api_token)
    available_banks = bp.available_banks(supported_banks)  # Available banks
    selected_bank = available_banks[0]
    session_id = bp.create_session(selected_bank, api_token)
    output = bp.get_consent(api_token, session_id)

    return render(request, 'welcome.html', {"e": email,'link':output})


def signup(request):
    return render(request, 'signup.html')


def postsignUp(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    postalCode = request.POST.get('postalCode')
    country = request.POST.get('country')

    user = auth.create_user_with_email_and_password(email, passw)
    uid = user['localId']

    data = {'Firstname': firstname, 'Lastname': lastname, 'PostalCode': postalCode, 'Country': country,
            'IBAN': 'TR' + str(random.randint(1 << 77, 1 << 79))}

    db.child('Customers').child(uid).child('Information').set(data)

    return render(request, 'signIn.html')


def dashboard(request):
    if c==0:
        account = bp.connect_account()
        print(account)
        funds=bp.available_funds(account, 100)
    else:
        pass
    return render(request, 'dashboard.html',{'count':c,'account':account})


def welcome(request):


    return render(request, 'welcome.html')
