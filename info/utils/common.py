# 共用的自定义工具
from flask import session, current_app

from info.models import User
import functools
from flask import g

def do_index_class(index):
    '''返回指定索引对应的类名'''

    if index == 0:
        return 'first'
    elif index == 1:
        return 'second'
    elif index == 2:
        return 'third'

    return ''


def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id', None)
        user = None
        if user_id:
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user
        return f(*args, **kwargs)
    return wrapper
