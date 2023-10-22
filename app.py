from pywebio.input import input, select, textarea
from pywebio.output import put_text, put_image, put_html, put_code, put_buttons, popup, put_progressbar, set_progressbar, toast, put_success, put_error, put_warning, put_info
from pywebio.input import textarea
from pywebio.output import put_success, put_warning, put_error
import redis
import secrets
from flask import Flask
from pywebio.platform.flask import webio_view
import argparse
from pywebio import start_server
from pywebio.session import run_js, set_env
import os

app = Flask(__name__)

# Access environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Define a Redis key for storing the data-to-code mapping
REDIS_MAPPING_KEY = "data_to_code_mapping"

# Create a Redis client connection
redis_client = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)

# CSS styles for improved appearance
custom_css = """
<style>
body {
    background-color: #f5f5f5;
    font-family: Arial, sans-serif;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.header {
    text-align: center;
    font-size: 36px;
    margin-bottom: 20px;
}

.secret-container {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    margin-top: 20px;
}

.code {
    font-size: 24px;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin: 20px 0;
}

.actions {
    text-align: center;
    margin-top: 20px;
}

.error-message {
    color: #d9534f;
    font-size: 20px;
}

.success-message {
    color: #5bc0de;
    font-size: 20px;
}

.warning-message {
    color: #f0ad4e;
    font-size: 20px;
}
</style>
"""

def save_mapping_to_redis(data_to_code):
    # Save the data-to-code mapping to Redis
    redis_client.hmset(REDIS_MAPPING_KEY, data_to_code)

def btn_click(btn_val):
    if btn_val == 'Home':
        run_js('window.location.reload()')
    elif btn_val == "About":
        popup("About",
              [put_html('<h2>Created by InsightIQ</h2>'),
               put_text("Project is implemented using Python and Redis"),
              ]
             )
    elif btn_val == 'Copy':
        toast("Code copied to clipboard", color='warning', duration=3)

def retrieve_mapping_from_redis():
    # Retrieve the data-to-code mapping from Redis
    data = redis_client.hgetall(REDIS_MAPPING_KEY)
    return data

def generate_code_and_store_data(data, data_to_code):
    # Generate a random code and store the data-to-code mapping in Redis
    code = secrets.token_hex(4)  # Generate an 8-character hexadecimal code
    data_to_code[code] = data
    save_mapping_to_redis(data_to_code)
    return code

def insert_data():
    # Input form to insert data and generate a code
    data = textarea("Enter your Secret", rows=5, placeholder="", required=True)

    data_to_code = retrieve_mapping_from_redis()
    code = generate_code_and_store_data(data, data_to_code)

    put_code(code, code_style="code")

    put_success("Secret Created 🔒. Copy and share the secret code to retrieve your secret!")
    put_buttons(['Home', 'About', 'Copy'], onclick=btn_click, class_="actions")

def retrieve_data():
    # Input form to retrieve data using a code
    code = input("Enter the secret code to retrieve your data:", type='text', required=True)
    data_to_code = retrieve_mapping_from_redis()
    data = data_to_code.get(code)

    if data:
        put_text(data, class_="code")
        put_success("Secret retrieved Successfully 🔓", class_="success-message")
    else:
        put_error("Invalid Code. Please verify the token 🔒", class_="error-message")

    put_buttons(['Home', 'About', 'Copy'], onclick=btn_click, class_="actions")

def home():
    put_html(custom_css)

    put_html('<div class="container">')
    put_html('<div class="header">SECRET KEEPER</div>')

    img = open('logo.png', 'rb').read()
    put_image(img, width='100px')

    put_code("Secret Keeper is a Python based web application to create and share secrets✨", code_style="python")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8083)
    args = parser.parse_args()

    start_server(home, port=args.port, debug=True)
