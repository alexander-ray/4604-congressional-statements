import re
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from newspaper import fulltext

class Scraper:
    # Get speech as list given a url
    def _get_text(self, url):
        try:
            # Getting text of page
            html = urllib.request.urlopen(url).read()
            text = fulltext(html)

            return text
        except Exception as e:
            return "Exception occurred \n" +str(e)

    # Function to retrieve relevant urls from page
    def _get_entries(self, base_url):
        try:
            content = urllib.request.urlopen(base_url).read()
            soup = BeautifulSoup(content, 'html.parser')

            entries = []
            # Find table rows
            rows = soup.find_all('tr')
            for t in rows:
                # Get info from row
                #party = t.find('td', {'class': 'party'}).contents[0]
                party = t["class"]
                #member = t.find('td', {'class': 'member'}).find('a').contents[0]
                #date = t.find('td', {'class': 'date'}).find('small').contents[0]
                #state = t.find('td', {'class': 'state'}).contents[0]
                #title = t.find('td', {'class': 'title'}).find('a').contents[0]
                #url = t.find('td', {'class': 'title'}).find('a')["href"]
                url = t.find_all('td')[-1].find('a')["href"]
                # Add to list as dictionary
                #entries.append({"party": party, "member": member, "date": date, "state": state, "title": title,
                #                "url": url, "text": self._get_text(url)})
                entries.append({"party": party, "text": self._get_text(url)})
            return entries
        except Exception as e:
            return "Exception occurred \n" + str(e)

    # Driver function to move get_urls through propublica pages
    def get_entries_driver(self, base_url, num):
        page_count = 1
        urls = []
        while page_count <= num:
            # Extend url list with urls from new page
            urls.extend(self._get_entries(base_url + str(page_count)))
            page_count += 1

        return urls
