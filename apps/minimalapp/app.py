from flask import (Flask, render_template,
                   url_for,
                   current_app, g,
                   request, redirect,
                   flash,
                   make_response,
                   session)

from email_validator import validate_email, EmailNotValidError

import logging
from flask_debugtoolbar import DebugToolbarExtension

import os

from flask_mail import Mail, Message


app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

app.logger.setLevel(logging.DEBUG)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Mail 클래스의 컨피그를 추가한다
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")


toobar = DebugToolbarExtension(app)
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])  # route
def index():
    return "Hello!!"


@app.route("/hello/<string:name>",
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"Hello!! Hello!! {name}"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


# request context
with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="KC", page="1"))


# application context
ctx = app.app_context()
ctx.push()
print(current_app.name)

# global context
g.connection = "connection"
print(g.connection)


with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))


# POST func
@app.route('/contact')
def contact():
    # 응답 오브젝트를 취득한다
    response = make_response(render_template("contact.html"))

    # 쿠키를 설정한다
    response.set_cookie("flaskbook key", "flaskbook value")

    # 세션을 설정한다
    session["username"] = "KC"

    # 응답 오브젝트를 반환한다
    return response


# redirect & request.form
@app.route('/contact/complate', methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        description = request.form['description']

        # 입력 체크
        is_valid = True
        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # 메일을 보낸다
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        # 문의 완료 엔드포인트로 리다이렉트한다
        flash("문의 내용은 메일로 송신했습니다. 문의해 주셔서 감사합니다.")
        # contact 엔드포인트로 리다이렉트한다
        return redirect(url_for("contact_complete"))

    return render_template('contact_complete.html')


def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
