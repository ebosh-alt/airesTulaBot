from flask import Flask

from routes.main import main_rt
from routes.new import new_rt
from routes.update import update_rt


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = '6t5t347821209i0ewdojakcfguyr7380ywhidoJLKCSN'  # Установите секретный ключ

    app.register_blueprint(main_rt, url_prefix='/')
    app.register_blueprint(update_rt, url_prefix='/')
    app.register_blueprint(new_rt, url_prefix='/')

    return app
