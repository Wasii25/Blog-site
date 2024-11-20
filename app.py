from flask import Flask, render_template, request
import requests
import smtplib
import os

MYEMAIL = os.environ['MYEMAIL']
PASSWORD = os.environ['PASSWORD']
message_sent = False

url = "https://api.npoint.io/3ea82762896f173f6480"

response = requests.get(url)
response.raise_for_status()  # Ensures an exception for HTTP errors
posts = response.json()

def smtp(toemail, name, email, phone, message):
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MYEMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MYEMAIL,
            to_addrs=toemail,
            msg=f"Subject:Blog Website Message\n\n"
                f"Name: {name}\n\n"
                f"Email: {email}\n\n"
                f"Phone: {phone}\n\n"
                f"Message: {message}"
        )
        global message_sent
        message_sent = True
app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', all_posts=posts)

@app.route('/about')
def about(): return render_template('about.html')




@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        n=1
        error = None
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        smtp(toemail=email, message=message, name=name, email=email, phone=phone)
        if message_sent:
            m = "Successfully sent message"
        else:
            m = "Message not sent, please try again later"

        return render_template('contact.html', message=m, n=1)


if __name__ == '__main__':
    app.run(detach=True)
