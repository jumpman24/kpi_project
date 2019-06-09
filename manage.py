from flask import Flask

from views import index_bp, players_bp, tournaments_bp

import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask('kpi_project')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.register_blueprint(index_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(tournaments_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.secret_key = os.urandom(24)
    app.run('0.0.0.0', '8000', debug=True)
