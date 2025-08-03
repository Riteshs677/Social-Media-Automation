import instaloader
import openpyxl
import json
import os

# ========== CONFIG ==========
EXCEL_FILE = "instagram_profiles.xlsx"  # Input Excel file
CACHE_FILE = "post_cache.json"         # Tracks downloaded posts
MAX_COLUMNS_TO_TRY = 1                 # Max columns to check (A, B, C)
MEDIA_ROOT = "media"                   # Download folder
MAX_POSTS_TO_DOWNLOAD = 1              # Set to N posts you want (e.g., 2)
# ============================

os.makedirs(MEDIA_ROOT, exist_ok=True)


if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        post_cache = set(json.load(f))
else:
    post_cache = set()

loader = instaloader.Instaloader(
    download_comments=False,
    download_geotags=False,
    download_pictures=True,
    download_video_thumbnails=False,
    save_metadata=False
)

def extract_shortcode(url):
    """Extract Instagram post shortcode from URL"""
    parts = url.strip("/").split("/")
    return parts[-1] if parts else None

def extract_urls_from_columns(file_path, max_columns):
    """Read Instagram URLs from Excel columns"""
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    urls_by_column = []

    for col in ws.iter_cols(min_row=2, max_col=max_columns):  
        col_urls = []
        for cell in col:
            if cell.value and isinstance(cell.value, str) and "instagram.com" in cell.value:
                col_urls.append(cell.value.strip())
        urls_by_column.append(col_urls)
    
    return urls_by_column

def download_n_posts(columns_of_urls, n):
    """Download N valid posts using row-wise iteration"""
    downloaded_count = 0
    max_rows = max(len(col) for col in columns_of_urls) if columns_of_urls else 0
    
    for row in range(max_rows):
        for col_index in range(len(columns_of_urls)):
            if downloaded_count >= n:
                return downloaded_count
                
            if row < len(columns_of_urls[col_index]):
                url = columns_of_urls[col_index][row]
                shortcode = extract_shortcode(url)
                
                if not shortcode:
                    continue
                if shortcode in post_cache:
                    print(f" Skipping cached post: {shortcode}")
                    continue
                
                print(f" Trying: {shortcode} (Column {col_index+1}, Row {row+1})")
                try:
                    post = instaloader.Post.from_shortcode(loader.context, shortcode)
                    loader.download_post(post, target=shortcode)
                    print(f" Downloaded: {shortcode}")
                    post_cache.add(shortcode)
                    downloaded_count += 1
                except Exception as e:
                    print(f" Failed to download {shortcode}: {str(e)}")
    return downloaded_count

# Main execution
columns_of_urls = extract_urls_from_columns(EXCEL_FILE, MAX_COLUMNS_TO_TRY)

# Change to media directory for downloads
os.chdir(MEDIA_ROOT)

downloaded = download_n_posts(columns_of_urls, MAX_POSTS_TO_DOWNLOAD)

if downloaded > 0:
    print(f" Successfully downloaded {downloaded} post(s)!")
else:
    print(" No new posts found in any column.")


os.chdir("..")
with open(CACHE_FILE, "w") as f:
    json.dump(list(post_cache), f)
