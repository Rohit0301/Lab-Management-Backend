import hashlib
from django.utils.encoding import smart_str


def get_hexdigest(algorithm, salt, raw_password):

    raw_password, salt = raw_password.encode(), salt.encode()
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError(
                '"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")
