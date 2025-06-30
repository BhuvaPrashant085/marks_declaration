from flask import Flask, render_template, request, session,render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

@app.route('/', methods=['GET', 'POST'])
def student_details():
    if request.method == 'POST':
        receiver_email = request.form['email']  # Get the email entered in the form
        
        sender_email = "prashantbhuva085@gmail.com"
        password = "kapq slzz abcr xzhs"  # Your email password
        
        # Generate a random OTP for email
        random_number = random.randint(100000, 999999)
        session['otp'] = random_number  # Store OTP in 
        
        # Mock student data (replace with actual student data logic)
        student = {
            "name": "John Doe",
            "email": receiver_email,
            "enrollment_number": "123456",
        }

        session['student'] = student  # Store student data in session
        
        body = f"Your code is: {random_number}"
        
        # Compose the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Test Email from Python"
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return render_template("verify_otp.html", email=receiver_email)  # Pass email to verify OTP


    # Render the form template if GET request
    return render_template_string(''' 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Student Details</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px; }
                .container { background: #fff; padding: 20px; border-radius: 10px; width: 300px; margin: auto; }
                h2 { text-align: center; }
                .student-info { margin-top: 20px; padding: 10px; background: #e0ffe0; border-radius: 5px; }
                .error { color: red; text-align: center; }
                .input-group { margin-bottom: 15px; }
                label { font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Enter Enrollment Number or Email</h2>
                <form method="POST">
                    <div class="input-group">
                        <label for="enrollmentNumber">Enrollment Number:</label>
                        <input type="text" name="enrollmentNumber" placeholder="Enter Enrollment Number" required>
                    </div>

                    <div class="input-group">
                        <label for="email">Or Email:</label>
                        <input type="email" name="email" placeholder="Enter Email" required>
                    </div>

                    <input type="submit" value="Submit">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        entered_otp = request.form['otp']
        
        # Check if entered OTP matches the stored OTP in session
        if session.get('otp') == int(entered_otp):
            return render_template("student.html",  email=email)
        else:
            return render_template("verify_otp.html", error="Invalid OTP", email=email)

    return render_template("verify_otp.html")

if __name__ == '__main__':
    app.run(debug=True)
