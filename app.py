import os
from pywebio.input import input, select, textarea
from pywebio.output import put_text, put_image, put_html, put_code, put_buttons, popup,put_progressbar,set_progressbar,toast,put_info
from pywebio.input import textarea
from pywebio.output import put_success,put_warning,put_error
import redis,time
import secrets
from flask import Flask
from pywebio.platform.flask import webio_view
import argparse
from pywebio import start_server
from pywebio.session import run_js, set_env
#import pyperclip




app = Flask(__name__)

# Access environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Define a Redis key for storing the data-to-code mapping
REDIS_MAPPING_KEY = "data_to_code_mapping"

# Create a Redis client connection
redis_client = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)

def save_mapping_to_redis(data_to_code):
    # Save the data-to-code mapping to Redis
    redis_client.hmset(REDIS_MAPPING_KEY, data_to_code)


# Add a new function to copy text to clipboard using JavaScript
def copy_to_clipboard(text_to_copy):
    js_code = f'''
        var textArea = document.createElement("textarea");
        textArea.value = "{text_to_copy}";
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
    '''
    run_js(js_code)


#------------------------------------------BUTTON CLICK EVENT
def btn_click(btn_val,code_to_copy):
            if btn_val == 'Home':
                run_js('window.location.reload()')
            elif btn_val == "About":
                popup("About",
                      [put_html('<h2>Created by InsightIQ Version-2.0</h2>'),
                       put_text("Project is implemented using Python and Redis"),
                                       
                       
                       ]

                      )
            elif btn_val== 'Copy':
                 copy_to_clipboard(code_to_copy)
                 toast("Code copied to clipboard",  color='warning', duration=3)
                 
  
#--------------------------------------REDIS DATA MAPPING

def retrieve_mapping_from_redis():
    # Retrieve the data-to-code mapping from Redis
    data = redis_client.hgetall(REDIS_MAPPING_KEY)
    return {code: data for code, data in data.items()}


def generate_code_and_store_data(data, data_to_code):
    # Generate a random code and store the data-to-code mapping in Redis
    code = secrets.token_hex(4)  # Generate an 8-character hexadecimal code
    data_to_code[code] = data
    save_mapping_to_redis(data_to_code)
    return code

#-------------------------------INSERT SECRET

def insert_data():
       # Input form to insert data and generate a code
    data = textarea("Enter your Secret", rows=5, placeholder="", required=True)

    data_to_code = retrieve_mapping_from_redis()
    code = generate_code_and_store_data(data, data_to_code)
     # Adding Progress bar
    import time

    put_progressbar('bar');
    for i in range(1, 11):
        set_progressbar('bar', i / 10)
        time.sleep(0.05)

    put_text("")
    put_text("")
    put_text("")
    put_text(f"")    
    larger_text = f'<span style="font-size: 50px; color: black;">{code}</span>'
    put_html(larger_text)   
    copied_code=data 
    put_success("Secret Created 🔒. Copy and share the secret code to retreive your secret!")    
    #put_buttons(['Home', 'About', 'Copy'], onclick=btn_click)
    put_buttons(['Home', 'About','Copy'], onclick=lambda btn_val: btn_click(btn_val, code))
    
  


 #--------------------------------RETREIVE SECRET
   
def retrieve_data():
    # Input form to retrieve data using a code
    code = input("Enter the secret code to retrieve your data:", type='text',required=True)
    data_to_code = retrieve_mapping_from_redis()
    data = data_to_code.get(code)   
     # Adding Progress bar
    import time

    put_progressbar('bar');
    for i in range(1, 11):
        set_progressbar('bar', i / 10)
        time.sleep(0.05)
    
    if data:          
       
        larger_text = f'<span style="font-size: 20px; color: black;">{data}</span>'
        put_text(" ")
        put_success("Secret retrieved Successfully 🔓")  
        put_html(larger_text)               
        put_text(" ")  
        
        put_buttons(['Home', 'About'], onclick=lambda btn_val: btn_click(btn_val, code))
           
    else:
        put_text(" ")
        larger_text = f'<span style="font-size: 20px; color: black;">No Secrets Found</span>'
        put_html(larger_text)
        put_text(" ")
        put_error("Invalid Code. Please verify the token 🔒")
        put_text(" ")
        put_buttons(['Home', 'About'], onclick=lambda btn_val: btn_click(btn_val, code))
        



#---------------------------HOME PAGE
def home():
    set_env(title="Secret Keeper")
   
    

    larger_text= f'<span style="font-size: 60px; color: black; display: block; text-align: center; margin: 0 auto;">SECRET KEEPER</span>'
    put_html(larger_text)


    img = open('logo.png', 'rb').read()
    put_image(img, width='100px')  # size of image

    put_code("Secret Keeper is a Python based web application to create and share secrets✨", 'python')   

    #view secret count
    count_of_data = redis_client.hlen(REDIS_MAPPING_KEY)
    put_text("Total Number of Secrets: ", count_of_data)
 


    option = select('Select an Option!', ['Create Secret', 'Retrieve Secret'])
    
    if option == 'Create Secret':
        insert_data()
    elif option == 'Retrieve Secret':
        retrieve_data()

# To allow reloading of the web browser and specifying the port
app.add_url_rule('/home', 'webio_view', webio_view(home), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8083)
    args = parser.parse_args()

    start_server(home, port=args.port, debug=True)
