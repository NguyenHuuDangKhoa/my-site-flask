from flask import Flask, render_template, request
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

# Configure email settings
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ds-projects")
def portfolio():
    return render_template("portfolio.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["message"])
        return render_template("index.html", section_id="contact", msg_sent=True)
    return render_template("index.html", section_id="contact")


def send_email(name, email, message):
    email_message = (
        f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    )
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=RECIPIENT_EMAIL,
            msg=email_message,
        )


if __name__ == "__main__":
    app.run(debug=True)
