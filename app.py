from flask import Flask, render_template, request, flash, redirect
import pandas as pd
from email_sender import send_bulk_email

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # required for flashing messages

# Configure your Gmail credentials
SENDER_EMAIL = 'kncfuturetech@gmail.com'
SENDER_PASSWORD = 'aukf xlau qzke aiwv'  # use Gmail App Password if 2FA is enabled

def load_template():
    with open('mail_template.txt', 'r') as f:
        lines = f.readlines()
        subject = lines[0].replace("Subject:", "").strip()
        body = ''.join(lines[1:]).strip()
        return subject, body

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    file = request.files['file']
    try:
        df = pd.read_excel(file)
        if 'Email' not in df.columns:
            flash("Excel file must contain a column named 'Email'")
            return redirect('/')
        emails = df['Email'].dropna().unique().tolist()
        subject, body = load_template()
        send_bulk_email(SENDER_EMAIL, SENDER_PASSWORD, emails, subject, body)
        flash("Emails sent successfully to first 500 addresses!")
    except Exception as e:
        flash(f"Error: {str(e)}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
