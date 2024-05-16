# Facebook Comment Crawler

This Python script crawls Facebook comments from multiple users using their cookies.

## Requirements

- Python 3.6 or higher
- Selenium 4.20.0
- openpyxl
- requests

## Usage

Prepare your cookies:

- Open your Facebook profile.
- Open your browser's developer tools (usually by pressing F12).
- Go to the "Network" tab and select request have cookie, then copy Cookie string

Create an Excel file named "cookies.xlsx" with two columns: "Name" and "Value."

- Add a row for each user, entering their "Name" and Cookie string in the "Value" column.

Run the script:

- Run the Python script.
- The script will prompt you to select the "cookies.xlsx" file.
- It will then ask for the save location for the resulting Excel file containing the comments.

Output
The script generates an Excel workbook sheets:

- Summary: Contains the username and the total number of comments made by each user.
- Individual User Sheets: For each user, a separate sheet displays the details of their comments:
  - Nơi comment: The name of the group or page where the comment was posted.
  - Nội dung: The content of the comment.
  - Số lượng: The number of times the same comment was posted.

## Notes

- This script uses Selenium to automate the browsing process and access Facebook content.
- You need to have chrome browser
- Facebook's terms of service may change, so this script might stop working at some point.
