from flask import Flask, render_template, request
from jinja2 import TemplateNotFound

from logger import logger
from dividend_checker import DividendChecker

app = Flask(__name__)

INDEX_TEMPLATE_NAME: str = "index.html"
dividend_checker: DividendChecker = DividendChecker()

@app.errorhandler(404)
def page_not_found(error):
    return "This page doesn't exist"

def try_load_template(template_name: str, **context) -> str:
    try:
        logger.info("Attempting to display home page")
        return render_template(template_name_or_list=template_name, **context)
    except TemplateNotFound:
        logger.error(msg=f"Template: {template_name} not found")
        return page_not_found()

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return try_load_template(INDEX_TEMPLATE_NAME)
    else:
        ticker_symbol = request.form.get('ticker_symbol').upper()

        if ticker_symbol == "":
            error_msg = "Please enter a ticker symbol"
            logger.info("User didn't enter a ticker symbol")
            return try_load_template(INDEX_TEMPLATE_NAME, error_msg=error_msg)

        dividend_dict = dividend_checker.get_dividend_dictionary(ticker_symbol)
        if len(dividend_dict) > 0:
            logger.info("Attempting to display dividend list")
            return try_load_template(INDEX_TEMPLATE_NAME, ticker_symbol=ticker_symbol, dividend_dict=dividend_dict)
        else:
            error_msg = f"Please enter a valid ticker symbol. You entered {ticker_symbol}"
            logger.info(f"User entered invalid ticker symbol {ticker_symbol}")
            return try_load_template(INDEX_TEMPLATE_NAME, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)