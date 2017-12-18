import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from newspaper import fulltext


class Scraper:
    # Get speech as list given a url
    @staticmethod
    def _get_text(url):
        try:
            # Getting text of page
            html = urllib.request.urlopen(url).read()
            # Using newpaper to get relevant text
            text = fulltext(html)
            return text
        except Exception as e:
            return "Exception occurred \n" + str(e)

    # Function to retrieve relevant urls from page
    # Iterates through rows
    def _get_entries(self, base_url):
        try:
            # Get content
            content = urllib.request.urlopen(base_url).read()
            soup = BeautifulSoup(content, 'html.parser')

            entries = []
            # Get list of table rows
            rows = soup.find_all('tr')
            for t in rows:
                # Get info from row
                # Specific to ProPublica's website
                party = t["class"][0]
                url = t.find_all('td')[-1].find('a')["href"]
                member = t.find_all('td')[1].find('a').contents[1].strip()
                # Add to list as dictionary
                entries.append({"party": party, "member": member, "text": self._get_text(url)})
            return entries
        except Exception as e:
            return "Exception occurred \n" + str(e)

    # Driver function to move get_urls through propublica pages
    def get_entries_driver(self, base_url, num, base_file):
        page_count = 1
        counter = 0

        test = []
        train = []

        while page_count <= num:
            print(page_count)
            # Get entries, add to list if valid
            new_entries = [x for x in self._get_entries(base_url + str(page_count * 5))
                           if not isinstance(x, str) and self._valid_entry(x['text'])]

            # Split into training and test
            for e in new_entries:
                # Ascii encoding to get rid of random weird chars
                e.update({k: e[k].encode('ascii', 'ignore').decode() for k in e.keys()})

                if counter % 10 == 0:
                    test.append(e)
                else:
                    train.append(e)
                counter += 1

            page_count += 1

        # Write final lists to file
        with open(base_file + '_test.txt', mode='w') as fout:
            json.dump(test, fout)
        with open(base_file + '_train.txt', mode='w') as fout:
            json.dump(train, fout)

    @staticmethod
    def _valid_entry(self, text):
        # Remove exceptions, entries <100 words
        if "exception" in text or "Exception" in text or len(text) < 100:
            return False
        else:
            return True
