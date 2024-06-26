from bs4 import BeautifulSoup
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

def scrape_flipkart(product_name):
    try:
        url = f"https://www.flipkart.com/search?q={product_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Update this class name based on the current HTML structure of Flipkart
        price_element = soup.find("div", {"class": "_Nx9bqj"})
        if price_element:
            price = price_element.text.strip()
            return price
        else:
            print(f"Price element not found for product: {product_name}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def index():
    product_name = request.args.get('product_name')
    if product_name:
        flipkart_price = scrape_flipkart(product_name)
        if flipkart_price:
            return f"The price of {product_name} on Flipkart is {flipkart_price}."
        else:
            return f"Could not retrieve the price for {product_name}."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
