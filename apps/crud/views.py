from apps.crud.models import User
from apps.app import db
from flask import Blueprint, render_template


# Blueprint로 crud 앱을 생성한다
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# index 엔드포인트를 작성하고 index.html을 반환한다
@crud.route("/")
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해 주세요"
