import requests

# Replace with your actual test endpoint
BASE_URL = "https://sllhub-test-f6581ed38b5d.herokuapp.com/api/test/ping"

# Replace with valid credentials from your config vars
HEADERS = {
    "X-Contact-Email": "qa1@vendorcorp.com",
    "X-Access-Token": "token-abc123"
}

def test_access():
    response = requests.get(BASE_URL, headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    print("Response Headers:", response.headers)
    print("Response Body:", response.text)

if __name__ == "__main__":
    test_access()
