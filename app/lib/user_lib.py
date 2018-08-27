from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User


class UserCreationException(Exception):
    pass


def create_user(user_dict):
    name = user_dict.get('name')
    if not name:
        raise UserCreationException('"name" is required')

    email = user_dict.get('email')
    if not email:
        raise UserCreationException('"email" is required')

    username = user_dict.get('username')
    if not username:
        raise UserCreationException('"username" is required')

    password = user_dict.get('password')
    if not password:
        raise UserCreationException('"password" is required')

    user = User(
        name=name,
        email=email,
        username=username,
        password=generate_password_hash(password)
    )

    return user
