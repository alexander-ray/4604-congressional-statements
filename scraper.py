import re
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from readability import Document

# Get speech as list given a url
def get_speech(url):
    try:
        # Getting text of page
        content = urllib.request.urlopen(url).read()
        #soup = BeautifulSoup(content, 'html.parser')
        doc = Document(content)
        doc.title()
        #page = soup.findAll('p')
        #txt = ''
        #for e in page:
        #    txt += e.get_text()
        #txt = page.replace('<p>','').replace('</p>','').replace('<br>','').replace('</br>','').replace('</div>','').replace('</span><hr noshade="noshade" size="1"/>','').strip()

        # Return list of lowercase words without punctuation
        return doc.summary()
    except Exception as e:
        return "Exception occurred \n" +str(e)


def save_remarks(url, label, train_fn, test_fn):
    remark_urls = get_relevant_urls(url)
    remarks_train = []
    remarks_test = []
    c = len(remark_urls)
    # Put 1/10 speeches in test set
    for i in range(0, c):
        if (i % 10 == 0):
            remarks_test.append([label, get_speech(remark_urls[i])])
        else:
            remarks_train.append([label, get_speech(remark_urls[i])])
    with open(train_fn, 'w') as fout:
        json.dump(remarks_train, fout)
    with open(test_fn, 'w') as fout:
        json.dump(remarks_test, fout)

# Function to retrieve relevant urls from page
def get_entries(base_url):
    try:
        content = urllib.request.urlopen(base_url).read()
        soup = BeautifulSoup(content, 'html.parser')

        entries = []
        # Find table rows
        rows = soup.find_all('tr')
        for t in rows:
            # Get info from row
            party = t.find('td', {'class': 'party'}).contents[0]
            member = t.find('td', {'class': 'member'}).find('a').contents[0]
            date = t.find('td', {'class': 'date'}).find('small').contents[0]
            state = t.find('td', {'class': 'state'}).contents[0]
            title = t.find('td', {'class': 'title'}).find('a').contents[0]
            url = t.find('td', {'class': 'title'}).find('a')["href"]
            # Add to list as dictionary
            entries.append({"party": party, "member": member, "date": date, "state": state, "title": title,
                            "url": url, "text": ""})

        return entries
    except Exception as e:
        return "Exception occurred \n" +str(e)

# Driver function to move get_urls through propublica pages
def get_entries_driver(base_url, num):
    page_count = 1
    urls = []
    while (page_count <= num):
        # Extend url list with urls from new page
        urls.extend(get_entries(base_url + str(page_count)))
        page_count += 1

    return urls

def main():
    #print(get_speech("https://www.cardin.senate.gov/newsroom/press/release/cardin-calls-on-fcc-to-reject-so-called-internet-freedom-order-to-keep-the-internet-truly-open"))
    print(get_entries("https://projects.propublica.org/represent/statements?page=1"))
    #print(len(get_urls_driver("https://projects.propublica.org/represent/statements?page=", 5)))
if __name__ == "__main__":
    main()