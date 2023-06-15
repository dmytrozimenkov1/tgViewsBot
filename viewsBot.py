from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'
session = requests.session()
session.verify = False

def first_get_request(url):
    # Custom headers
    headers = {
        'Host': 't.me',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru',
        'Connection': 'keep-alive',
        'User-Agent': USER_AGENT
    }

    try:
        # Perform GET request with headers
        response = session.get(url, headers=headers)
        return response
    except Exception as e:
        # If an error occurs while making the GET request
        return {'error': 'An error occurred while trying to perform the GET request.', 'details': str(e)}

def second_get_request(url):
    # Custom headers
    headers = {
        'Host': 't.me',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru',
        'Connection': 'keep-alive',
        'User-Agent': USER_AGENT,
        'Referer': url
    }

    try:
        # Perform GET request with headers
        response = session.get(url + "?embed=1&mode=tme", headers=headers)
        return response
    except Exception as e:
        # If an error occurs while making the GET request
        return {'error': 'An error occurred while trying to perform the GET request.', 'details': str(e)}
def third_post_request(url):
    # Custom headers
    headers = {
        'Host': 't.me',
        'Origin': 'https://t.me',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': USER_AGENT,
        'Referer': url + "?embed=1&mode=tme",
        'Content-Length': '5',
        'Accept-Language': 'ru',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Perform POST request with headers and data
        response = session.post(url + "?embed=1&mode=tme", headers=headers, data={'_rl': '1'})
        return response
    except Exception as e:
        # If an error occurs while making the POST request
        return {'error': 'An error occurred while trying to perform the POST request.', 'details': str(e)}

def fourth_get_request(url, token):
    # Custom headers
    headers = {
        'Host': 't.me',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': USER_AGENT,
        'Referer': url + "?embed=1&mode=tme",
        'Accept-Language': 'ru',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        # Perform GET request with headers
        response = session.get(f"https://t.me/v/?views={token}", headers=headers)
        return response
    except Exception as e:
        # If an error occurs while making the GET request
        return {'error': 'An error occurred while trying to perform the GET request.', 'details': str(e)}



def extract_view_count(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    view_count_element = soup.find('span', {'class': 'tgme_widget_message_views'})

    if view_count_element:
        return int(view_count_element.text)
    else:
        return None


def extract_token(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    message_element = soup.find('div', {'class': 'tgme_widget_message'})

    if message_element and 'data-view' in message_element.attrs:
        return message_element['data-view']
    else:
        return None

@app.route('/start', methods=['POST'])
def start():
    global session
    session = requests.session()
    data = request.get_json()

    if 'url' in data:
        url = data['url']

        second_response_before = second_get_request(url)
        if 'error' in second_response_before:
            return jsonify(second_response_before), 400

        view_count_before = extract_view_count(second_response_before.text)
        token = extract_token(second_response_before.text)

        if not token:
            return jsonify({'error': 'No token found.'}), 400

        third_response = third_post_request(url)

        if 'error' in third_response:
            return jsonify(third_response), 400

        fourth_response = fourth_get_request(url, token)
        if 'error' in fourth_response:
            return jsonify(fourth_response), 400

        second_response_after = second_get_request(url)
        if 'error' in second_response_after:
            return jsonify(second_response_after), 400

        view_count_after = extract_view_count(second_response_after.text)

        if view_count_before is None or view_count_after is None:
            return jsonify({'error': 'Could not determine view count.'}), 400

        view_added = view_count_after > view_count_before

        return jsonify({
            'view_added': view_added,
            'total_views': view_count_after
        }), 200 if view_added else 400
    else:
        return jsonify({'error': 'No url provided.'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)