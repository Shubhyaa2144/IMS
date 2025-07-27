import smtplib
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
PORT = 2525
USERNAME = "47a83bba588807"  # Replace with your Mailtrap username
PASSWORD = "79523af71f18fa"  # Replace with your Mailtrap password


try:
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls()  # Start TLS encryption
        server.login(USERNAME, PASSWORD)
        print("Successfully connected to Mailtrap SMTP!")
except Exception as e:
    print(f"Error connecting to Mailtrap SMTP: {str(e)}")
