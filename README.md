# Reddit Image Downloader

This Python script allows you to bulk download images from a specified Reddit subreddit and save them with the correct filenames.

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - praw
  - requests
  - selenium
  - beautifulsoup4

## Getting Started

1. Clone the repository or download the script.
2. Install the required packages using `pip install -r requirements.txt`.
3. Obtain Reddit API credentials:
   - Go to the [Reddit Developer Console](https://www.reddit.com/prefs/apps).
   - Click on "Create App" or "Create Another App."
   - Choose the "script" option.
   - Fill in the required information.
   - The "client ID" and "client secret" will be displayed on the app details page.
4. Replace the placeholder credentials in the script with your actual Reddit API credentials.
5. Run the script using `python reddit_image_downloader.py`.
6. Enter the subreddit name, limit, and click "Download Images."

## Features

- Downloads images in bulk from a specified subreddit.
- Saves images with filenames based on the post titles.
- Uses a headless Chrome browser to dynamically fetch the user agent.

## Additional Notes

- Ensure that you have the necessary permissions to access and download content from the specified subreddit.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

