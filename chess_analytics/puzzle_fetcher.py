import sys
import time
import html
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


class PuzzleFetcher:
    """ Fetching recent failed puzzles for a user from standard Puzzles and Puzzle Rush."""
    def __init__(self, user, chromedriver_path = '/usr/local/bin/chromedriver'):
        self.chromedriver_path = chromedriver_path
        self.user = user
        self.driver = self.instantiate_webdriver()

    def instantiate_webdriver(self):
        """Instantiate a Selenium webdriver from chromedriver."""
        s = Service(self.chromedriver_path)

        # Create chrome webdriver with some default options.
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        return webdriver.Chrome(executable_path=self.chromedriver_path, options=chrome_options)

    # Puzzle grabbing functions
    def get_user_puzzles(self):
        """Find out which puzzles they recently attempted (also navigates driver to that page)."""
        url = f"https://www.chess.com/stats/puzzles/{self.user}"
        page = self.driver.get(url)
        time.sleep(2)
        return pd.read_html(self.driver.page_source)[0]

    def navigate_to_puzzle_rush_table(self):
        # Navigate to their puzzles page
        url = f"https://www.chess.com/stats/puzzles/{self.user}"
        page = self.driver.get(url)
        time.sleep(2)
        # Click the rush tab
        element = self.driver.find_element_by_id("tab-rush")
        safe_click(self.driver, element)

    def get_user_puzzle_rush_scores(self):
        self.navigate_to_puzzle_rush_table()
        return pd.read_html(self.driver.page_source)[0]

    def get_failed_puzzles(self, limit=10):
        """Generate a list of failed puzzles from Puzzle Rush."""
        self.navigate_to_puzzle_rush_table()
        # Elements of rows (tr), where each is a separate puzzle rush. 
        elmnts = self.driver.find_elements_by_xpath("//table/tbody/tr")
        failed_puzzles = []
        for i in range(min(len(elmnts), 10)):
            self.navigate_to_puzzle_rush_table()
            elmnts = self.driver.find_elements_by_xpath("//table/tbody/tr")
            failed_puzzles.extend(element_to_failed_puzzles_dataset(elmnts[i], self.driver))
        return failed_puzzles


# Selenium navigation helpers
def navigate_to_last_opened(driver):
    """Given a driver, navigate to last opened window (e.g. from a click())."""
    time.sleep(2)
    window_after = driver.window_handles[-1]
    driver.switch_to.window(window_after)
    
def safe_click(driver, element):
    """Scrolls into view before clicking an element."""
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element) 


# Puzzle grabbing functions
def element_to_failed_puzzles_dataset(element, driver):
    """ Given an element that is a link to puzzle rush, generate an array describing 
    failed puzzles.
    """
    # Navigate to specific puzzle rush page
    element.click()
    navigate_to_last_opened(driver)
    source_rush = driver.current_url
    source_rush_window = driver.window_handles[-1]
    
    # Get failed puzzles
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    puzzle_divs = soup.find_all("div", {"class": "streak-indicator-streak streak-indicator-incorrect streak-indicator-link"})
    puzzle_ratings = [puzzle_div.text.strip() for puzzle_div in puzzle_divs]
    failure_links = driver.find_elements_by_class_name('streak-indicator-incorrect')
    
    # Iterate through failed puzzles to create dataset
    failed_puzzle_dataset = []
    for puzzle_rating, failure_element in zip(puzzle_ratings, failure_links):
        # Navigate to each failed puzzle to get link (hacky)
        time.sleep(3)
        safe_click(driver, failure_element)
        navigate_to_last_opened(driver)
        failed_puzzle_dataset.append((puzzle_rating, driver.current_url, source_rush))
        # Switch back to source
        time.sleep(1)
        driver.switch_to.window(source_rush_window)
    return failed_puzzle_dataset




def main():
    # Run by python puzzle_fetcher.py {your_username}
    user = sys.argv[1]
    puzzle_fetcher = PuzzleFetcher(user=user)
    failed_puzzles = puzzle_fetcher.get_failed_puzzles(limit=3)
    print(failed_puzzles)

if __name__=="__main__":
    main()