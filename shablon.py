import jinja2
from flask import Flask, render_template
from python_s.log import logger

# app = Flask(__name__)
#
#
# def get_template(file, args):
#     body = jinja2.Template(open(file).read()).render(args)
#     return body
#
#
# @app.route('/')
# def index():
#     context = {
#         'title': 'Новосной сайт',
#         'text': 'Скоро тут будут новости'
#     }
#     return get_template("Z:/Program/FAUST/flask_news_test/template/index.html", context)
#     # return render_template("Z:/Program/FAUST/flask_news_test/template/index.html", **context)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


data = open("Z:/Program/FAUST/flask_news_test/param_template/news").read()
logger.info(data)