import requests
import json

VERIFY_SSL = False

def add_view_to_post(post_url):
    # Define the url where the flask app is running

    # url = 'http://localhost:5001/start'
    url = "http://ec2-35-170-69-10.compute-1.amazonaws.com/start"
    # url = "http://172.31.3.120:80/start"
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


import boto3
def restart_ec2_instance(instance_id):
    ec2 = boto3.client('ec2', region_name='us-west-1')

    print("Stopping instance...")
    ec2.stop_instances(InstanceIds=[instance_id])

    waiter = ec2.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    print("Starting instance...")
    ec2.start_instances(InstanceIds=[instance_id])
# if __name__ == "__main__":
post_url = "https://t.me/globaltradecrypto/74"
add_view_to_post(post_url)

restart_ec2_instance("i-019ea4cc4bb7b17a6")

