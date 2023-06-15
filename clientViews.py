import requests
import json
VERIFY_SSL = False

def add_view_to_post(post_url):
    # Define the url where the flask app is running
    url = 'http://localhost:5001/start'

    # Define the payload to be sent to the server
    payload = {
        'url': post_url
    }

    # Make a POST request to the server
    response = requests.post(url, json=payload, verify=VERIFY_SSL)

    # If the request was successful
    if response.status_code == 200:
        # Get the JSON response body
        data = response.json()

        # Print the results
        print(f"View added: {data['view_added']}")
        print(f"Total views: {data['total_views']}")

    else:
        print("An error occurred while trying to add a view to the post.")



# if __name__ == "__main__":
post_url = "https://t.me/globaltradecrypto/74"
add_view_to_post(post_url)

