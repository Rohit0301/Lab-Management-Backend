from .models import Session
import uuid
from functools import wraps


def CreateOrGetSession(user_id, role):
    try:
        session_exist = Session.objects.filter(
            user_id=user_id, role=role, is_deleted=False).first()
        if (session_exist):
            return session_exist.session_id
        else:
            session_id = uuid.uuid4()
            Session.objects.create(
                user_id=user_id, role=role, session_id=session_id)
            return session_id
    except:
        raise Exception("Something went wrong!")


def FetchUserSession(request):
    try:
        auth_headers = request.headers.get('Authorization')
        if (not auth_headers):
            raise Exception("Invalid session!")
        session_id = auth_headers.split(' ')[1]
        session = Session.objects.get(
            session_id=session_id, is_deleted=False)
        return session
    except:
        raise Exception("Invalid session, please login again")
