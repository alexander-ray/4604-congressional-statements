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

def get_relevant_urls(base_url):
    try:
        content = urllib.request.urlopen(base_url).read()
        soup = BeautifulSoup(content, 'html.parser')

        urls = []
        # All relevant urls contain ws
        tags = soup.find_all(href=re.compile("ws"))
        for t in tags:
            if("Remarks" in t.string):
                urls.append(urllib.parse.urljoin(base_url, t['href']))

        return urls
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

def remarks_driver():
    save_remarks('http://www.presidency.ucsb.edu/2008_election_speeches.php?candidate=70&campaign=2008CLINTON&doctype=5000',
                'clinton', 'clinton_remarks_train', 'clinton_remarks_test')
    save_remarks('http://www.presidency.ucsb.edu/2008_election_speeches.php?candidate=44&campaign=2008OBAMA&doctype=5000',
                'obama1', 'obama1_remarks_train', 'obama1_remarks_test')
    save_remarks('http://www.presidency.ucsb.edu/2012_election_speeches.php?candidate=44&doctype=1150',
                'obama2', 'obama2_remarks_train', 'obama2_remarks_test')

def main():
    print(get_speech("https://www.cardin.senate.gov/newsroom/press/release/cardin-calls-on-fcc-to-reject-so-called-internet-freedom-order-to-keep-the-internet-truly-open"))
    print(get_speech("https://connolly.house.gov/news/documentsingle.aspx?DocumentID=1202"))
if __name__ == "__main__":
    main()