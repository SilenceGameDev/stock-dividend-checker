from flask import Flask, render_template, request
from jinja2 import TemplateNotFound

from logger import logger
from dividend_checker import DividendChecker

app = Flask(__name__)

INDEX_TEMPLATE_NAME: str = "index.html"
dividend_checker = DividendChecker()

@app.errorhandler(404)
def page_not_found(error):
    return "This page doesn't exist"

def try_load_template(template_name: str, **context) -> str:
    try:
        return render_template(template_name_or_list=template_name, **context)
    except TemplateNotFound:
        logger.error(msg=f"Template: {template_name} not found")
        return page_not_found()

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        ticker_symbol = ""
        return try_load_template(INDEX_TEMPLATE_NAME, ticker_symbol=ticker_symbol)
    else:
        ticker_symbol = request.form.get('ticker_symbol')
        # do stuff with ticker_symbol
        dividend_checker.check_stock(ticker_symbol)

        return try_load_template(INDEX_TEMPLATE_NAME, ticker_symbol=ticker_symbol)




if __name__ == '__main__':
    app.run(debug=True)