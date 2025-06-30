import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import sys
import json

# Dummy student data
student_data = {
    "230007001": { "name": "Anand", "marks": 85, "mobile": "9512340001", "email": "anand@example.com" },
    "230007002": { "name": "Prashant", "marks": 80, "mobile": "9512399064", "email": "prashantbhuva085@gmail.com" },
    "230007003": { "name": "Abhishek", "marks": 78, "mobile": "9512340003", "email": "abhishek@example.com" },
    "230007004": { "name": "Heer", "marks": 92, "mobile": "9512340004", "email": "heer@example.com" },
    "230007005": { "name": "Aman", "marks": 88, "mobile": "9512340005", "email": "aman@example.com" },
    "230007006": { "name": "dhara", "marks": 91, "mobile": "9512340006", "email": "dhara@example.com" },
    "230007007": { "name": "Dhruvi", "marks": 99, "mobile": "9512340007", "email": "dhruvi@example.com" }
}

# Get enrollment number from frontend (via sys.argv)
if len(sys.argv) < 2:
    print(json.dumps({ "status": "error", "message": "No enrollment number provided" }))
    sys.exit()

enroll = sys.argv[1]

if enroll not in student_data:
    print(json.dumps({ "status": "error", "message": "Enrollment not found" }))
    sys.exit()

student = student_data[enroll]
receiver_email = student["email"]

# Email credentials
sender_email = "prashantbhuva085@gmail.com"
password = "kapq slzz abcr xzhs"  # App password

# Create OTP and Email
otp = random.randint(100000, 999999)
subject = "Your OTP Code for Marks Portal"
body = f"Hello {student['name']},\n\nYour OTP is: {otp}\n\nRegards,\nAdmin"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print(json.dumps({ "status": "success", "otp": otp }))
except Exception as e:
    print(json.dumps({ "status": "error", "message": str(e) }))
