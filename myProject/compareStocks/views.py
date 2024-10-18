from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import yfinance as yf
from openai import OpenAI
from .models import StockInfo, StockAnalysis


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# views.py

from .models import StockInfo


# views.py

from django.shortcuts import render
def stock_analysis_prompt(company_a, company_b):
    format_instruction = """
    <h2>Stock Analysis: Company A vs. Company B</h2>

    <h3>Market Capitalization</h3>
    <p>[Brief description of market capitalization comparison]</p>

    <h3>Price-to-Earnings (P/E) Ratios</h3>
    <p>[Comparison of trailing and forward P/E ratios]</p>

    <h3>PEG Ratio</h3>
    <p>[Comparison of PEG ratios]</p>

    <h3>Price-to-Sales and Price-to-Book Ratios</h3>
    <p>[Analysis of price-to-sales and price-to-book ratios]</p>

    <h3>Performance Indicators</h3>
    <p>[Discussion of 52-week range and performance indicators]</p>

    <h3>Average Stock Prices</h3>
    <p>[Analysis of fifty-day and two-hundred-day averages]</p>

    <h3>Conclusion</h3>
    <p>[Final summary and investor guidance]</p>

    <h3>What to do next</h3>
    <p>[suggest how to continue research. Give specific suggestions in the context of what was said in this doc.  Incorporate my aphliate link to <a href="https://www.tradingview.com/?aff_id=142766">TradingView</a>no markdown</p>"""
    return f"Compare the stocks of {company_a} and {company_b}.\n{format_instruction}"

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    try:
        stock_info = stock.info
        data = {
            'longName': stock_info.get('longName', 'N/A'),
            'marketCap': stock_info.get('marketCap', None),
            'enterpriseValue': stock_info.get('enterpriseValue', None),
            'trailingPE': stock_info.get('trailingPE', None),
            'forwardPE': stock_info.get('forwardPE', None),
            'pegRatio': stock_info.get('pegRatio', None),
            'priceToSalesTrailing12Months': stock_info.get('priceToSalesTrailing12Months', None),
            'priceToBook': stock_info.get('priceToBook', None),
            'enterpriseToRevenue': stock_info.get('enterpriseToRevenue', None),
            'enterpriseToEbitda': stock_info.get('enterpriseToEbitda', None),
            'fiftyTwoWeekHigh': stock_info.get('fiftyTwoWeekHigh', None),
            'fiftyTwoWeekLow': stock_info.get('fiftyTwoWeekLow', None),
            'fiftyDayAverage': stock_info.get('fiftyDayAverage', None),
            'twoHundredDayAverage': stock_info.get('twoHundredDayAverage', None)
        }

        # Save to database
        stock_info_obj, created = StockInfo.objects.update_or_create(
            ticker=ticker,
            defaults=data
        )

        return data
    except Exception as e:
        return {"error": f"Failed to retrieve stock data: {str(e)}"}
def definitions(request):
    return render(request, 'def.html')

def index(request):
    ticker1 = None
    ticker2 = None
    fundamental_data1 = None
    fundamental_data2 = None
    analysis_html=None

    if request.method == "POST":
        ticker1 = request.POST.get('ticker1')
        ticker2 = request.POST.get('ticker2')

        # Check if data exists in the database
        try:
            stock_info1 = StockInfo.objects.get(ticker=ticker1)
            fundamental_data1 = stock_info1.__dict__
        except StockInfo.DoesNotExist:
            fundamental_data1 = get_stock_info(ticker1)

        try:
            stock_info2 = StockInfo.objects.get(ticker=ticker2)
            fundamental_data2 = stock_info2.__dict__
        except StockInfo.DoesNotExist:
            fundamental_data2 = get_stock_info(ticker2)

        # Format numerical values
        for data in [fundamental_data1, fundamental_data2]:
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    data[key] = f"{value:,.2f}"
        
        # Check for existing analysis
        existing_analysis = StockAnalysis.objects.filter(ticker1=ticker1, ticker2=ticker2).first()
        if existing_analysis:
            analysis_html = existing_analysis.analysis
        else:
            prompt = stock_analysis_prompt(ticker1, ticker2)
            message = prompt + str(fundamental_data1) + str(fundamental_data2)
            client = OpenAI()
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful stock market assistant."},
                    {"role": "user", "content": message}
                ]
            )
            analysis_html = completion.choices[0].message.content

            # Save the analysis to the database
            StockAnalysis.objects.create(
                ticker1=ticker1,
                ticker2=ticker2,
                analysis=analysis_html
            )

        return render(request, 'index.html', {
            'ticker1': ticker1,
            'ticker2': ticker2,
            'data1': fundamental_data1,
            'data2': fundamental_data2,
            'analysis': analysis_html
        })
    return render(request, 'index.html')

def definitions(request):
    return render(request, 'def.html')

