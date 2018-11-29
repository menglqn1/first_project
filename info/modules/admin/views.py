import time
from datetime import datetime, timedelta

from flask import g, render_template, request, session, url_for, redirect, current_app

from info.models import User
from info.modules.admin import admin_blu
from info.utils.common import user_login_data


@admin_blu.route('/user_count')
def user_count():
    total_count = 0
    try:
        total_count = User.query.filter(User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)

    mon_count = 0
    t = time.localtime()
    begin_mon_date_str = '%d-%02d-01' % (t.tm_year, t.tm_mon)
    begin_mon_date = datetime.strptime(begin_mon_date_str, '%Y-%m-%d')

    try:
        mon_count = User.query.filter(User.is_admin == False, User.current_time > begin_mon_date).count()
    except Exception as e:
        current_app.logger.error(e)

    day_count = 0
    begin_day_date = datetime.strptime(('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)), '%Y-%m-%d')

    try:
        day_count = User.query.filter(User.is_admin == False, User.create_time > begin_day_date).count()
    except Exception as e:
        current_app.logger.error(e)

    active_time = []
    active_count = []

    today_date_str = ('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday))
    today_date = datetime.strptime(today_date_str, '%Y-%m-%d')

    for i in range(0, 31):
        # 取到某一天的0点0分
        begin_date = today_date - timedelta(day=i)
        # 取到下一天的0点0分
        end_date = today_date - timedelta(days=(i-1))
        count = User.query.filter(User.is_admin == False, User.last_login >= begin_date, User.last_login < end_date).count()
        active_count.append(count)
        active_time.append(begin_date.strftime('%Y-%m-%d'))

        active_time.reverse()
        active_count.reverse()

        data = {
            'total_count': total_count,
            'mon_count': mon_count,
            'day_count': day_count,
            'active_time': active_time,
            'active_count': active_count
        }

        return render_template('admin/user_count.html', data=data)


@admin_blu.route('/index')
@user_login_data
def index():
    user = g.user
    return render_template('admin/index.html', user=user.to_dict())


@admin_blu.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = session.get('user_id', None)
        is_admin = session.get('is_admin', False)
        if user_id and is_admin:
            return redirect(url_for('admin.index'))

        return render_template('admin/login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not all([username, password]):
        return render_template('admin/login.html', errmsg='参数错误')

    try:
        user = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template('admin/login.html', errmsg='用户信息查询失败')

    if not user:
        return render_template('admin/login.html', errmsg='未查询到用户信息')

    if not user.check_passowrd(password):
        return render_template('admin/login.html', errmsg='用户名或者密码错误')

    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name
    session['is_admin'] = user.is_admin

    return redirect(url_for('admin.index'))
