from flask import request, current_app, make_response, jsonify

from info import redis_store, constants
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu


@passport_blu.route('/image_code')
def get_image_code():
    # 1.获取到当前的图片编号id
    code_id = request.args.get('code_id')
    # 2.生成验证码
    name, text, image = captcha.generate_captcha()

    try:
        redis_store.setex('ImageCode_' + code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.loggin.error(e)
        return make_response(jsonify(errno=RET.DATAERR, errmsg='保存图片验证失败'))
    # 返回响应内容
    resp = make_response(image)
    # 设置内容类型
    resp.headers['Content-Type'] = 'image/jpg'
    return resp