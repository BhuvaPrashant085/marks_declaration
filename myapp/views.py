from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Sample student data
students = {
    "230007001": {"name": "Rehan", "marks": 85, "email": "rehanramodiya666@gmail.com"},
    "230007002": {"name": "Prashant", "marks": 90, "email": "prashantbhuva085@gmail.com"},
    "230007016": {"name": "Ravi", "marks": 78, "email": "ravigehlot77770@gmail.com"},
    "230007004": {"name": "Heer", "marks":  92, "email": "chokshiheer741@gmail.com"},
    "230007001": {"name": "Anand", "marks": 88, "email": "anandtrambadiya036@gmail.com"},
    "230001065": {"name": "Dhara", "marks": 91, "email": "vagheladhara200@gmail.com"},
    "230007007": {"name": "Dhruvi", "marks": 99, "email": "dkachalia1234@gmail.com"},
    "230007003": {"name": "Abhishek", "marks": 99, "email": "chhatbarabhishek4@gmail.com"}
}


def index(request):
    return render(request, 'index.html')

def send_email(request):
    if request.method == 'POST':
        enrollment_number = request.POST.get('enrollmentNumber')
        email = request.POST.get('email')

        print(f"Received Enrollment Number: {enrollment_number}")
        print(f"Received Email: {email}")

        # Validate both enrollment number and email
        if enrollment_number and email:
            if enrollment_number in students:
                student = students[enrollment_number]
                if student['email'] != email:
                    return render(request, 'index.html', {'error': "Email does not match the enrollment number."})
            else:
                return render(request, 'index.html', {'error': "Invalid Enrollment Number."})
        else:
            return render(request, 'index.html', {'error': "Please enter both enrollment number and email."})

        # Store student data in session
        request.session['student'] = student
        request.session['email'] = email
        request.session['enrollment_number'] = enrollment_number

        # Generate and store OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        print(f"Generated OTP: {otp}")

        # Send OTP email
        sender_email = "prashantbhuva085@gmail.com"
        receiver_email = email
        password = os.getenv('SMTP_PASSWORD')
        print("SMTP_PASSWORD:", password)  # Debug print

        if not password:
            return HttpResponse("SMTP password not set correctly. Please check your environment variable.")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Your OTP for Verification"
        body = f"Your OTP is: {otp}"
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            return render(request, 'verify_otp.html', {'email': email})
        except Exception as e:
            return HttpResponse(f"Failed to send email: {e}")

    return redirect('index')  # fallback


def verify_otp(request):
    email = request.session.get('email')
    student = request.session.get('student')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if int(entered_otp) == request.session.get('otp'):
            return render(request, 'student.html', {
                'email': email,
                'student': student
            })
        else:
            return render(request, 'verify_otp.html', {
                'email': email,
                'error': "Invalid OTP"
            })

    return render(request, 'verify_otp.html', {'email': email})
