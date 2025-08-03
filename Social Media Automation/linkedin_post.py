import json
import requests
import os
from linkedin_auth import load_credentials, get_access_token

def get_headers(access_token):
    return {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }

def get_user_info(headers):
    url = 'https://api.linkedin.com/v2/userinfo'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def upload_images(image_paths, headers, author_urn):
    assets = []
    for path in image_paths:
        register_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
        register_body = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": author_urn,
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }

        reg_response = requests.post(register_url, headers=headers, json=register_body)
        reg_response.raise_for_status()
        value = reg_response.json()['value']
        upload_url = value['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_urn = value['asset']

        with open(path, 'rb') as f:
            upload_headers = {
                'Authorizat\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ion': headers['Authorization'],
                'Content-Type': 'application/octet-stream'
            }
            upload_resp = requests.put(upload_url, headers=upload_headers, data=f)
            upload_resp.raise_for_status()

        assets.append(asset_urn)
    return assets

def create_image_post(author_urn, headers, caption, asset_urns):
    body = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": caption},
                "shareMediaCategory": "IMAGE",
                "media": [{"status": "READY", "media": urn} for urn in asset_urns]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=body)
    response.raise_for_status()
    post_id = response.headers.get("x-restli-id")
    print(f"\n Posted to LinkedIn: https://www.linkedin.com/feed/update/{post_id}")

def post_all_successful_downloads(media_root='media'):
    
    creds = load_credentials()
    access_token = get_access_token(creds)
    if not access_token:
        print(" No access token found.")
        return

    headers = get_headers(access_token)
    user_info = get_user_info(headers)
    author_urn = f"urn:li:person:{user_info['sub']}"

    print(f" Authenticated as: {user_info.get('name', 'Unknown User')}")

    successful = 0
    for folder in sorted(os.listdir(media_root)):
        folder_path = os.path.join(media_root, folder)
        if not os.path.isdir(folder_path):
            continue

        txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]
        if not txt_files:
            print(f" Skipping {folder}: No .txt file found for caption.")
            continue

        caption_file = os.path.join(folder_path, txt_files[0])
        try:
            with open(caption_file, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
        except Exception as e:
            print(f" Error reading caption from {caption_file}: {e}")
            continue

        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if not image_files:
            print(f" No image files found in {folder}, skipping.")
            continue

        try:
            print(f"\n Uploading post from folder: {folder}")
            asset_urns = upload_images(image_files, headers, author_urn)
            create_image_post(author_urn, headers, caption, asset_urns)
            successful += 1
        except Exception as e:
            print(f" Error uploading {folder}: {e}")
            continue

    print(f"\n Done: {successful} LinkedIn post(s) created.")

if __name__ == "__main__":
    post_all_successful_downloads(media_root='media')

















