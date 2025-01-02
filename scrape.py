import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from PIL import Image
import io
import re

# Constants
BASE_DIR = "/app/automation"

def create_folder(folder_path):
    """Create folder if it doesn't exist"""
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
    except Exception as e:
        print(f"Error creating folder {folder_path}: {e}")

def clean_filename(url):
    """Extract and clean filename from URL"""
    # Get the base filename from URL
    filename = os.path.basename(url.split('?')[0])
    
    # Remove any invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # If filename is empty or invalid, create a timestamp-based name
    if not filename or filename == '':
        timestamp = int(time.time() * 1000)
        extension = '.jpg'
        filename = f"image_{timestamp}{extension}"
    
    return filename

def download_image(url, folder_path):
    try:
        # Get clean filename from URL
        filename = clean_filename(url)
        base_name, extension = os.path.splitext(filename)
        
        # If no extension or invalid extension, default to .jpg
        if not extension or extension.lower() not in ['.jpg', '.jpeg', '.png']:
            extension = '.jpg'
            filename = base_name + extension
        
        # Create full filepath
        filepath = os.path.join(folder_path, filename)
        
        # If file exists, add number to filename
        counter = 1
        while os.path.exists(filepath):
            new_filename = f"{base_name}_{counter}{extension}"
            filepath = os.path.join(folder_path, new_filename)
            counter += 1
        
        response = requests.get(url)
        if response.status_code == 200:
            # Save the image directly to the file
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f"Downloaded: {os.path.basename(filepath)}")
            return True
            
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def scrape_images(url, folder_name):
    try:
        # Create folder
        website_folder = os.path.join(BASE_DIR, folder_name)
        create_folder(website_folder)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.find_all(['img', 'picture'])
        downloaded_count = 0
        
        for img in images:
            if img.name == 'picture':
                img_tag = img.find('img')
                if img_tag:
                    img = img_tag
            
            for attr in ['src', 'data-src', 'srcset']:
                img_url = img.get(attr)
                if img_url:
                    if ',' in img_url:
                        img_url = img_url.split(',')[0].split(' ')[0]
                    img_url = urljoin(url, img_url)
                    
                    if is_valid_image_url(img_url):
                        if download_image(img_url, website_folder):
                            downloaded_count += 1
                            time.sleep(1)
                            break
        
        print(f"Completed scraping folder {folder_name}: Downloaded {downloaded_count} images")
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def is_valid_image_url(url):
    """Check if the URL points to a valid image file"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.path.lower().endswith(('.png', '.jpg', '.jpeg'))

def main():
    try:
        # Ensure base directory exists
        create_folder(BASE_DIR)
        print(f"Base directory: {BASE_DIR}")
        
        websites = [
            {
                "folder": "milka",
                "url": "https://www.milka.bg/vsichki-produkti"
            },
            {
                "folder": "lindt",
                "url": "https://www.chocolate.lindt.com/our-chocolate"
            },
            {
                "folder": "biobenjamin",
                "url": "https://biobenjamin.com/products/"
            }
        ]
        
        # Create folders
        for website in websites:
            website_folder = os.path.join(BASE_DIR, website['folder'])
            create_folder(website_folder)
        
        # Start scraping
        for website in websites:
            print(f"\nProcessing {website['folder']}...")
            scrape_images(website['url'], website['folder'])
            time.sleep(2)
            
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()