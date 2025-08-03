import json

def load_credentials(filename='credentials.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def get_access_token(credentials):
    return credentials.get('access_token')

if __name__ == '__main__':
    creds = load_credentials()
    token = get_access_token(creds)
    if token:
        print("Access token loaded successfully.")
    else:
        print("Access token not found in credentials.json.")
