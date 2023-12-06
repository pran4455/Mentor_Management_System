from django.shortcuts import render
from django.http import HttpResponse
import csv
import datetime
import smtplib
import os
from email.message import EmailMessage
import random

# Create your views here.
def home(request):
    return render(request, 'login2.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Read the register.csv file
        with open('register.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                print(username)
                print(password)
                
                stored_username = row[3]
                stored_password = row[4]

                print('stored is :',stored_username)
                print('stored_pass :',stored_password)
                print(len(stored_password))
                print('len of input password',len(password))
                print(stored_password == password)

                if username == stored_username:
                    if password == stored_password:
                        with open('logs.csv', 'a') as logs:
                            write = csv.writer(logs)
                            date_time = datetime.datetime.now()

                            current_time = date_time.time()
                            current_date = date_time.date()

                            write.writerow([username, current_date, current_time])

                            global CURRENT_USER, CURRENT_PRIV
                            CURRENT_USER = username

                        if row[-1] == "admin":
                            CURRENT_PRIV = "admin"
                            return render(request, "admin_homepage.html")
                        elif row[-1] == "mentor":
                            CURRENT_PRIV = "mentor"
                            return render(request, "mentor_homepage.html")
                        elif row[-1] == "mentee":
                            CURRENT_PRIV = "mentee"
                            return render(request, "mentee_homepage.html")
                    else:
                        return render(request, 'login2.html', {'alertmessage': 'Wrong password'})  # Display wrong password message

            return render(request, 'login2.html', {'alertmessage': 'Username not found'})  # Display username not found message

    return render(request, 'login2.html')


def addstudent(request):
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        address = request.POST['address']
        age = request.POST['age']
        gender = request.POST['gender']
        blood_group = request.POST['blood-group']

        if password != confirm_password:
            return render(request, 'register.html', {'alertmessage': 'Passwords do not match.'})

        try:
            with open('register.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if email == row[3]:
                        return render(request, 'register.html', {'alertmessage': 'E-mail already exists.'})
        except:
            ...

        with open('register.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, mobile, dob, email, password, address, age, gender, blood_group, "mentee"])

        return render(request, 'login2.html', {'alertmessage': 'New user registration information stored successfully.'})

    return render(request, 'register.html')
