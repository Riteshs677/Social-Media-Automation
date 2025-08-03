import subprocess
import os
import shutil

def cleanup_media_folder(media_dir="media"):
    if not os.path.exists(media_dir):
        print("📁 Media folder does not exist, nothing to clean.")
        return

    for folder in os.listdir(media_dir):
        folder_path = os.path.join(media_dir, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"🧹 Deleted: {folder_path}")

    print("✅ Media folder cleaned after successful upload.")

try:
    print("📥 Step 1: Extracting Instagram post URLs...")
    subprocess.run(['python', 'url.py'], check=True)

    print("📸 Step 2: Downloading Instagram media...")
    subprocess.run(['python', 'insta.py'], check=True)

    print("📤 Step 3: Posting to LinkedIn...")
    subprocess.run(['python', 'linkedin_post.py'], check=True)

    print("✅ All steps completed successfully!")

    # ✅ Step 4: Cleanup after all success
    cleanup_media_folder()

except subprocess.CalledProcessError as e:
    print(f"❌ Error in one of the steps: {e}")

