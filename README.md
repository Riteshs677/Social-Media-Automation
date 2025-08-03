# Social-Media-Automation
Deliver the right content at the right time to the right channel.

Absolutely! Here's a **detailed and simple `README.md`** for your GitHub project that covers setup, configuration, usage, and folder structure clearly.

---

### ✅ `README.md`

```markdown
# 🚀 Instagram to LinkedIn Automation

This project automates the process of:

1. Scraping **Instagram posts** (images and captions) from URLs stored in an Excel file.
2. Avoiding duplicate downloads using a **cache system**.
3. Uploading downloaded media and captions as **LinkedIn posts** using the LinkedIn API.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/insta-to-linkedin.git
cd insta-to-linkedin
````

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have Python 3.8+.

---

### 3. Prepare Your Credentials

Create a file named `credentials.json` in the root directory:

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "redirect_uri": "your_redirect_uri",
  "access_token": "your_access_token"
}
```

> 💡 Use LinkedIn Developer Portal to create your app and get these values.

---

### 4. Add Instagram URLs

Place your public Instagram post/reel URLs inside an Excel file `urls.xlsx` under the `scraper/` folder. Each column should represent one account (e.g., `techcrunch`, `googledeepmind`, etc.).

Example:

| techcrunch                                                                         | googledeepmind                                                                         |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [https://www.instagram.com/p/ABCDE12345/](https://www.instagram.com/p/ABCDE12345/) | [https://www.instagram.com/reel/WXYZ67890/](https://www.instagram.com/reel/WXYZ67890/) |

---

## 🧪 How to Use

### Step 1: Download Instagram Posts

Run the scraper to download **new posts only**:

```bash
python scraper/insta.py
```

✔ Will:

* Read Instagram URLs from `urls.xlsx`
* Skip posts already downloaded (via `post_cache.json`)
* Save each post to `media/{shortcode}/` folder with image and caption

---

### Step 2: Upload to LinkedIn

Once posts are downloaded, upload them to LinkedIn:

```bash
python linkedin/linkedin_post.py
```

✔ Will:

* Read folders inside `media/`
* Extract `.jpg` and `.txt` file
* Upload post (text + image) to your LinkedIn feed
* Show links to published posts

---

## 💡 Customization

* `MAX_COLUMNS_TO_TRY`: Controls how many **Instagram accounts (columns)** to try per run.
* `MAX_DOWNLOADS`: Controls how many **successful downloads** before breaking.
* These values can be edited in `scraper/insta.py`.

---

## 🛡️ Safety

* Your Instagram posts must be **public**.
* Only **image** posts are supported (video coming soon).
* Duplicate posts are avoided using `post_cache.json`.

---

## 🧼 Optional Cleanup

To auto-delete folders in `media/` after uploading to LinkedIn, enable cleanup in `linkedin_post.py`:

```python
DELETE_AFTER_UPLOAD = True
```

---

## 📌 To Do

* [ ] Support videos (.mp4)
* [ ] Refresh LinkedIn token automatically
* [ ] Telegram bot alerts for upload success/failure

---

## 📬 Questions?

Create an issue or message [yourname](https://github.com/yourusername).

---

## 📜 License

MIT License

```

---

Let me know:
- Your GitHub username to personalize the link
- If you want a badge (e.g., Python version, license)
- If you want GIF/image demos in README

I'll adjust the final version accordingly.
```
