from django.shortcuts import redirect, render
from home.models import Transactions, Users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import secrets
import pymongo
import datetime
from django.db import transaction
from django.db import connection


# Create your views here.
def home(request):
    try:
        user = Users.objects.get(email=request.session['email'])
        #
        cursor = connection.cursor()
        cursor.execute('CALL getTrxnHistory(%s)', [user.email])
        historys = cursor.fetchall()
        cursor.close()
        #
        return render(request, 'home.html', {'user': user, 'historys': historys})
    except:
        messages.error(request, 'You need to login first')
        return redirect('../validation')

# validation function


def validation(request):
    return render(request, 'validation.html')

# login function


def signin(request):
    if request.method == 'POST':
        try:
            user = Users.objects.get(email=request.POST.get('email'))
            if check_password(request.POST.get('pwd'), (user.password)):
                request.session['email'] = user.email
                print('Logged in successfully...!')
                return redirect('../')
            else:
                messages.error(request, 'Password incorrect...!')
        except Users.DoesNotExist as e:
            messages.error(request, 'No user found of this email....!')
    return redirect('../validation')

# signup function


def register(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('pwd') and request.POST.get('phone'):
            saveUser = Users()

            saveUser.name = request.POST.get('name')
            saveUser.email = request.POST.get('email')
            saveUser.password = make_password(request.POST.get('pwd'))
            saveUser.phoneNumber = request.POST.get('phone')
            saveUser.balance = 500
            saveUser.accountNo = secrets.token_hex(8)

            if saveUser.isExists():
                messages.error(request, request.POST.get(
                    'email') + " email address already registered ! Please Log in.")
                return redirect('../validation')
            else:
                saveUser.save()
                messages.success(
                    request, 'Your account registered successfully ! Please Log in now.')
                return redirect('../validation')
    else:
        return redirect('../validation')


def logout(request):
    try:
        del request.session['email']
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "An error occurred. Try again.")
        return redirect('validation')
    return redirect('validation')


def sharedMoney(request):
    try:
        user = Users.objects.get(email=request.session['email'])
        if request.method == 'POST':
            if request.POST.get('sender') and request.POST.get('receiver') and request.POST.get('amount'):

                with transaction.atomic():
                    try:
                        try:
                            receiver = Users.objects.get(
                            email=request.POST.get('receiver'))
                        except:
                            messages.error(request, 'No user found of this email....!')
                            return render(request, 'sharedMoney.html', {'user': user})

                        trxn = Transactions()
                        trxn.sender = request.POST.get('sender')
                        trxn.receiver = request.POST.get('receiver')
                        trxn.amount = int(request.POST.get('amount'))

                        trxn.save()
                    except Exception as e:
                        messages.error(
                            request, 'Transaction failed. ' + (str(e)).split(',')[1])
                        return render(request, 'sharedMoney.html', {'user': user})
                    messages.success(request, 'Amount transfered successfully')
                    return render(request, 'sharedMoney.html', {'user': user})
        else:
            return render(request, 'sharedMoney.html', {'user': user})

    except:
        messages.error(request, 'You need to login first')
        return redirect('../validation')


def chat_box(request):
    try:
        user = Users.objects.get(email=request.session['email'])

        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print(client)

        db = client['cash_transfer']
        collection = db['user_chat']

        if request.method == 'POST':

            if request.POST.get('name') and request.POST.get('messages') and request.POST.get('receiver'):
                nameSender = user.name
                email=request.session['email']
                name = request.POST.get('name')
                receiver = request.POST.get('receiver')
                msgs = request.POST.get('messages')

                now = datetime.datetime.utcnow()
            
                dictionary = {'nameSender':nameSender, 'email':email, 'name':name, 'receiver': receiver, 'messages': msgs, 'created_at': now}
                collection.insert_one(dictionary)
                
                
                messages.success(request, "Message send successfully...!")
                return redirect('/')
        
        return render(request, 'chat_box.html', {'user': user,})

    except:
        messages.error(request, 'You need to login first')
        return redirect('../validation')


def show_message(request):
    try:
        print("messages showing")
        user = Users.objects.get(email=request.session['email'])

        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print(client)

        db = client['cash_transfer']
        collection = db['user_chat']

        curRec = collection.find({'receiver': user.email})
        curSen = collection.find({'email': user.email})
        recMsg = [document for document in curRec]
        senMsg = [document for document in curSen]

        return render(request, 'show_message.html', {'user': user, 'recMsg': recMsg, 'senMsg': senMsg})
    except:
        messages.error(request, 'You need to login first')
        return redirect('../validation')
