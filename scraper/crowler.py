import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.coventry.ac.uk"

def get_course_links():
    url = "https://www.coventry.ac.uk/study-at-coventry/undergraduate-study/course-finder/"
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    links = set()

    # 🔥 target only course divs
    courses = soup.find_all("div", class_="course")

    for course in courses:
        a_tag = course.find("a", href=True)

        if a_tag:
            href = a_tag["href"]

            # convert relative → absolute
            if not href.startswith("http"):
                href = BASE_URL + href

            links.add(href)

    return list(links)[:5]