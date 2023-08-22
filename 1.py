from flask import Flask, request, jsonify
import requests
import concurrent.futures
import time

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except requests.exceptions.Timeout:
        pass  # Ignore URLs that timeout
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
    return []

def merge_unique_sorted_lists(lists):
    merged = []
    for lst in lists:
        merged.extend(lst)
    return sorted(set(merged))

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    numbers_lists = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            numbers_list = future.result()
            if numbers_list:
                numbers_lists.append(numbers_list)

    merged_numbers = merge_unique_sorted_lists(numbers_lists)
    response = {
        "numbers": merged_numbers
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8008)
