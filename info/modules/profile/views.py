import datetime

from flask import render_template, redirect, g, request, current_app, jsonify

from info import constants, db
from info.models import Category, News
from info.modules.profile import profile_blu
from info.utils.common import user_login_data
from info.utils.image_storage import storage
from info.utils.response_code import RET


@profile_blu.route('/news_list')
@user_login_data
def user_news_list():
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    user = g.user
    news_list = []
    current_page = 1
    total_page = 1
    try:
        paginate = News.query.filter(News.user_id == user.id).paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        news_list = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_review_dict())

    data = {
        'news_list': news_dict_li,
        'total_page': total_page,
        'current_page': current_page
    }

    return render_template('news/user_news_list.html', data=data)


@profile_blu.route('/news_release', methods=['GET', 'POST'])
@user_login_data
def news_release():
    if request.method == 'GET':
        categories = []
        try:
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)

        category_dict_li = []
        for category in categories:
            category_dict_li.append(category.to_dict())

        category_dict_li.pop(0)

        return render_template('news/user_news_release.html', data={'categories': category_dict_li})

    title = request.form.get('title')
    source = '个人发布'
    digest = request.form.get('digest')
    content = request.form.get('content')
    index_image = request.files.get('index_image')
    category_id = request.form.get('category_id')

    if not all([title, source, digest, content, index_image, category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    try:
        category_id = int(category_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    user = g.user
    time = datetime.datetime.now()
    file_name = 'index_image' + str(user.id) + str(time)

    try:
        index_image_data = index_image.read()
        storage(index_image_data, file_name)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    news = News()
    news.title = title
    news.digest = digest
    news.source = source
    news.content = content
    news.index_image_url = constants.QINIU_DOMIN_PREFIX + file_name
    news.category_id = category_id
    news.user_id = user.id
    news.status = 1

    try:
        db.session.add(news)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    return jsonify(errno=RET.OK, errmsg='OK')


@profile_blu.route('/collection')
@user_login_data
def user_collection():
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    user = g.user

    news_list = []
    total_page = 1
    current_page = 1
    try:
        paginate = user.collection_news.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        current_page = paginate.page
        total_page = paginate.pages
        news_list = paginate.items
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        'total_page': total_page,
        'current_page': current_page,
        'collections': news_dict_li
    }
    return render_template('news/user_collection.html', data=data)


@profile_blu.route('/pass_info', methods=['GET', 'POST'])
@user_login_data
def pass_info():
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not all([old_password, new_password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    user = g.user
    if not user.check_passowrd(old_password):
        return jsonify(errno=RET.PWDERR, errmsg='原密码错误')

    user.password = new_password
    return jsonify(errno=RET.OK, errmsg='保存成功')


@profile_blu.route('/pic_info', methods=['GET', 'POST'])
@user_login_data
def pic_info():
    user = g.user
    avatar_name = 'avatar' + str(user.id)
    if request.method == 'GET':
        return render_template('news/user_pic_info.html', data={'user_info': g.user.to_dict()})
    try:
        avatar = request.files.get('avatar').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    try:
        storage(avatar, avatar_name)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传头像失败')

    user.avatar_url = avatar_name
    return jsonify(errno=RET.OK, errmsg='OK', data={'avatar_url': constants.QINIU_DOMIN_PREFIX + avatar_name})


@profile_blu.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():
    user = g.user

    data = {
        'user_info': user.to_dict()
    }

    if request.method == 'GET':
        return render_template('news/user_base_info.html', data=data)

    nick_name = request.json.get('nick_name')
    signature = request.json.get('signature')
    gender = request.json.get('gender')

    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    if gender not in ('WOMAN', 'MAN'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender
    return jsonify(errno=RET.OK, errmsg='OK')


@profile_blu.route('/info')
@user_login_data
def user_info():
    user = g.user
    if not user:
        return redirect('/')

    data = {
        'user_info': user.to_dict() if user else None,
    }
    return render_template('news/user.html', data=data)
