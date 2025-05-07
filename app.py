from flask import Flask, render_template
import requests
import matplotlib.pyplot as plt
import os
from datetime import datetime

app = Flask(__name__)

# API URLs và keys
GOLD_API_URL = 'https://www.goldapi.io/api/XAU/USD'
GOLD_API_KEY = 'goldapi-5zxbsmadwnfc1-io'
CURRENCY_API_URL = 'https://v6.exchangerate-api.com/v6/22d8db1544bf4e2dddedb570/latest/USD'
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&current_weather=true'

# Định nghĩa bộ lọc chuyển đổi timestamp thành datetime
def timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Đăng ký bộ lọc với Flask
app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime

# Hàm lấy dữ liệu giá vàng
def get_gold_price():
    headers = {'x-access-token': GOLD_API_KEY}
    response = requests.get(GOLD_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {'error': f'Lỗi API: Mã {response.status_code} - {response.text}'}

# Hàm lấy dữ liệu tỷ giá
def get_currency_rate():
    response = requests.get(CURRENCY_API_URL)
    if response.status_code == 200:
        return response.json()
    return {'error': f'Lỗi API: Mã {response.status_code} - {response.text}'}

# Hàm lấy dữ liệu thời tiết
def get_weather():
    response = requests.get(WEATHER_API_URL)
    if response.status_code == 200:
        return response.json()
    return {'error': f'Lỗi API: Mã {response.status_code} - {response.text}'}

# Hàm tạo biểu đồ giá vàng
def create_gold_chart():
    years = [2019, 2020, 2021, 2022, 2023]
    gold_prices = [1500, 1700, 1800, 1900, 2000]
    
    plt.figure(figsize=(8, 5))
    plt.plot(years, gold_prices, marker='o', color='gold')
    plt.title('Biểu đồ giá vàng theo năm')
    plt.xlabel('Năm')
    plt.ylabel('Giá vàng (USD/ounce)')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    plt.savefig('static/gold_chart.png')
    plt.close()

@app.route('/')
def index():
    gold_data = get_gold_price()
    currency_data = get_currency_rate()
    weather_data = get_weather()
    
    create_gold_chart()
    
    return render_template('index.html', gold=gold_data, currency=currency_data, weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
    