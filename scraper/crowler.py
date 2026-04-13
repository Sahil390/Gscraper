import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.coventry.ac.uk"

def get_links():
    url = BASE + "/study-at-coventry/undergraduate-study/course-finder/"
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    links = set()

    # get only course blocks
    for c in soup.find_all("div", class_="course"):
        a = c.find("a", href=True)

        if not a:
            continue

        h = a["href"]

        if not h.startswith("http"):
            h = urljoin(BASE, h)

        links.add(h)

    return list(links)[:5]

# print(get_links())