from info import constants
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import index_blu
from flask import render_template, current_app, session, request, jsonify, g


@index_blu.route('/')
@user_login_data
def index():
    user = g.user

    news_list = None

    categories = Category.query.all()
    categories_dicts = []

    for category in categories:
        categories_dicts.append(category.to_dict())

    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())
    data = {'user_info': user.to_dict() if user else None,
            'click_news_list': click_news_list,
            'categories': categories_dicts
            }

    return render_template('news/index.html', data=data)


@index_blu.route('/news_list')
def news_list():
    """
      获取指定分类的新闻列表
      1. 获取参数
      2. 校验参数
      3. 查询数据
      4. 返回数据
      :return:
      """
    page = request.args.get('page', '1')
    per_page = request.args.get('per_page', constants.HOME_PAGE_MAX_NEWS)
    cid = request.args.get('cid', '1')

    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    filters = []
    if cid != 1:
        filters.append(News.category_id == cid)
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询失败')

    news_model_list = paginate.items
    total_page = paginate.pages
    current_page = paginate.page

    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        'total_page': total_page,
        'current_page': current_page,
        'news_dict_li': news_dict_li
    }

    return jsonify(errno=RET.OK, errmsg='OK', data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
