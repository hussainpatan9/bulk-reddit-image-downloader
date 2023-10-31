import praw
import requests
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def get_user_agent():
    """
    Retrieves the user agent using a headless Chrome browser.
    Returns:
        str: User agent string or None if an error occurs.
    """
    url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    try:
        # Create a Chrome driver instance
        with webdriver.Chrome(options=chrome_options) as driver:
            # Open the URL
            driver.get(url)

            # Wait for a while to ensure that the page is loaded
            driver.implicitly_wait(5)

            # Get the page source after the JS has executed
            page_source = driver.page_source

        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the element with id 'detected_value' and get its text
        detected_value = soup.find('div', {'id': 'detected_value'})

        if detected_value:
            return detected_value.text.strip()
        else:
            print("Could not find 'detected_value' element on the page.")
            return None

    except Exception as e:
        print(f"Error getting user agent: {e}")
        return None


def download_image(submission, output_directory, user_agent):
    """
    Downloads an image and saves it with the correct filename.
    Args:
        submission: PRAW submission object.
        output_directory (str): Directory to save the image.
        user_agent (str): User agent for HTTP headers.
    """
    title = submission.title
    image_url = submission.url

    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()

        file_extension = image_url.split('.')[-1]
        filename = f"{title}.{file_extension}"

        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        raise


def choose_output_directory():
    """
    Opens a dialog to choose the output directory.
    Returns:
        str: Chosen output directory or None if canceled.
    """
    return filedialog.askdirectory(title="Choose Output Directory")


def download_images():
    """
    Downloads images from a subreddit and saves them with the correct filename.
    """
    subreddit_name = entry_subreddit.get()
    limit = entry_limit.get()

    # Get user agent dynamically
    user_agent = get_user_agent()
    if not user_agent:
        messagebox.showerror(
            "Error", "Failed to get user agent. Check console for details.")
        return

    try:
        # Convert limit to an integer
        limit = int(limit)
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid limit. Please enter a valid number.")
        return

    # Set up PRAW credentials (replace with your own)
    reddit = praw.Reddit(
        # client_id="YOUR_CLIENT_ID",
        # client_secret="YOUR_CLIENT_SECRET",
        # password="YOUR_PASSWORD",
        # user_agent=user_agent,
        # username="YOUR_USERNAME",
    )

    # Choose output directory
    output_directory = choose_output_directory()
    if not output_directory:
        return  # User canceled the directory selection

    os.makedirs(output_directory, exist_ok=True)

    try:
        # Subreddit to download images from
        subreddit = reddit.subreddit(subreddit_name)

        # Iterate through all submissions in the subreddit
        for submission in subreddit.hot(limit=limit):
            try:
                # Handling rate limits
                while True:
                    try:
                        download_image(
                            submission, output_directory, user_agent)
                        break  # Break the loop if download is successful
                    except praw.exceptions.APIException as api_exception:
                        if "RATELIMIT" in str(api_exception):
                            print("Rate limit exceeded. Waiting for a while...")
                            # Wait for 60 seconds before retrying
                            time.sleep(60)
                        else:
                            raise  # Raise other API exceptions

            except Exception as e:
                print(f"Error processing submission: {e}")

        messagebox.showinfo("Success", "Bulk image download complete.")

    except praw.exceptions.PRAWException as e:
        messagebox.showerror("Error", f"PRAW error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# Create the main window
window = tk.Tk()
window.title("Reddit Image Downloader")

# Create and place UI elements
label_subreddit = tk.Label(window, text="Enter subreddit:")
label_subreddit.pack()

entry_subreddit = tk.Entry(window)
entry_subreddit.pack()

label_limit = tk.Label(window, text="Enter limit:")
label_limit.pack()

entry_limit = tk.Entry(window)
entry_limit.pack()

button_download = tk.Button(
    window, text="Download Images", command=download_images)
button_download.pack()

# Start the Tkinter event loop
window.mainloop()
