Based on your code, I'll create a detailed README.md that explains your image scraping project:

```markdown:README.md
# Chocolate Products Image Scraper

An automated web scraping tool designed to download product images from various chocolate manufacturer websites. Currently supports Milka, Lindt, and BioBenjamin product pages.

## Features

- Automated image scraping from multiple websites
- Intelligent image filename handling and deduplication
- Organized folder structure for downloaded images
- Built-in rate limiting to prevent server overload
- Supports various image URL patterns and formats (jpg, jpeg, png)
- Handles different image tag structures including `<img>` and `<picture>` elements

## Prerequisites

Before running this project, you need:

- Docker installed on your system
- OR Python 3.10+ with pip installed

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chocolate-scraper.git
cd chocolate-scraper
```

2. Build the Docker image:
```bash
docker build -t chocolate-scraper .
```

3. Run the container:
```bash
docker run -v $(pwd)/automation:/app/automation chocolate-scraper
```

### Manual Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

The scraper will automatically create folders and download images from:
- Milka (https://www.milka.bg/vsichki-produkti)
- Lindt (https://www.chocolate.lindt.com/our-chocolate)
- BioBenjamin (https://biobenjamin.com/products/)

Images will be saved in the following structure:
```
automation/
├── milka/
├── lindt/
└── biobenjamin/
```

## Configuration

You can modify the scraper by editing `scrape.py`:

1. Add new websites to scrape:
```python
websites = [
    {
        "folder": "new_brand",
        "url": "https://example.com/products"
    },
    # ... existing websites ...
]
```

2. Adjust the delay between downloads:
```python
time.sleep(1)  # Change the number of seconds between image downloads
```

3. Modify the user agent:
```python
headers = {
    'User-Agent': 'Your custom user agent string'
}
```
