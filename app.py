from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Say
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # Change this to your SMTP server
SMTP_PORT = 587
SENDER_EMAIL = 'eyosiasbitsu@gmail.com'  # Change this to your email
SENDER_PASSWORD = 'tdle iplq ettm ifea'  # Change this to your email password
RECIPIENT_EMAIL = 'fetsum@formulax.dev'  # Change this to the email where you want to receive notifications

def send_email_notification(caller_number):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'New Voicemail Received'
        
        body = f"""
        New voicemail received!
        
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        From: {caller_number}
        
        Please check your voicemail system to listen to the message.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email notification sent for call from {caller_number}")
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")


@app.route('/sms', methods=['POST'])
def sms():
    print(request.form)
    number = request.form['From']
    message_body = request.form['Body']

    resp = MessagingResponse()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    
    return str(resp)


@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    say = Say('Hi', voice='Polly.Emma')
    say.break_(strength='x-weak', time='100ms')
    say.p('this is protide lab, sorry we are not open right now, but please leave us a message.')
    say.break_(strength='x-weak', time='50ms')
    say.p('Thank You!')

    response.append(say)
    response.record()
    
    # Send email notification after recording
    caller_number = request.form.get('From', 'Unknown')
    send_email_notification(caller_number)
    
    response.hangup()

    return str(response)


@app.route('/')
def index():
    return """<p>Nexus Labs</p>
    """


if __name__ == '__main__':
    app.run(host='phone.tonyteaches.tech', port=5000)

