from app.models.user import User
from app.libs.auth import generate_token
from app.validtors.forms import LoginForm
from app.exceptions import IllegalArgumentException
from app.libs.web_response import WebResponse
from flask import current_app as app


@app.route('/')
def index():
    return 'hello world'


@app.route("/monitor/alive")
def alive():
    return "alive"


@app.route('/api/v1/login', methods=['POST'])
def login():
    form = LoginForm().validate_for_api()
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.validate_password(form.password.data):
        raise IllegalArgumentException('wrong password')
    token, expiration = generate_token(user)

    return WebResponse.build_data({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': expiration
    })
