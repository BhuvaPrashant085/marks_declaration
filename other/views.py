from flask import Flask, render_template, request, session, redirect, url_for
import random
import smtplib
from django.shortcuts import render
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Sample student data
students = {
    "12345": {"name": "John Doe", "marks": 90, "email": "john@example.com"},
    "67890": {"name": "Jane Smith", "marks": 85, "email": "jane@example.com"}
}

@app.route('/')

def index(request):
    return render(request, 'index.html')  # ✅ Now this works
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import random
from django.conf import settings

# Simulate student data (for illustration)
students = {
    '230007002': {'name': 'Prashant Bhuva', 'email': 'prashantbhuva085@gmail.com'}
    # Add more student records as needed
}

# Your Django view
def send_email(request):
    if request.method == 'POST':
        enrollment_number = request.POST.get('enrollmentNumber')
        email = request.POST.get('email')

        # If enrollment number is provided, get student details
        if enrollment_number in students:
            student = students[enrollment_number]
        elif email:
            student = None  # You can add email lookup logic here if needed
        else:
            return render(request, 'index.html', {'error': "Invalid Enrollment Number or Email"})

        # Generate random OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp  # Store OTP in session
        request.session['email'] = email  # Store email in session

        # Send OTP via email
        sender_email = settings.EMAIL_HOST_USER  # Use settings.py for configuration
        receiver_email = email
        subject = "Your OTP for Verification"
        message = f"Your OTP is: {otp}"

        try:
            send_mail(subject, message, sender_email, [receiver_email])
            return render(request, 'verify_otp.html', {'email': email})  # Pass email to verify page
        except Exception as e:
            return HttpResponse(f"Failed to send email: {e}")
    else:
        return render(request, 'index.html', {'error': 'Invalid request method'})

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    # Retrieve email and student data from session
    email = session.get('email')
    student = session.get('student')  # Retrieve student data from session

    if request.method == 'POST':
        entered_otp = request.form['otp']
        
        # Check if entered OTP matches the stored OTP in session
        if session.get('otp') == int(entered_otp):
            # Pass both email and student data to the template
            return render_template("student.html", email=email, student=student)
        else:
            return render_template("verify_otp.html", error="Invalid OTP", email=email)

    # If GET request, just render the OTP verification page
    return render_template("verify_otp.html", email=email)

if __name__ == '__main__':
    app.run(debug=True)
