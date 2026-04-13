import re
import requests
from bs4 import BeautifulSoup
from functools import lru_cache

INDIA_URL = "https://www.coventry.ac.uk/international-students-hub/entry-requirements/"
DOC_URL = "https://www.coventry.ac.uk/london/study/how-to-apply/document-checklist/"

sess = requests.Session()


def get_soup(u):
    r = sess.get(u, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml"), r.text


def get_dl(html, k):
    pats = [
        rf"'{re.escape(k)}'\s*:\s*'([^']*)'",
        rf'"{re.escape(k)}"\s*:\s*"([^"]*)"',
    ]
    for p in pats:
        m = re.search(p, html, re.DOTALL)
        if m:
            return m.group(1).strip()
    return "NA"


@lru_cache(maxsize=1)
def get_india():
    soup, _ = get_soup(INDIA_URL)
    b = soup.select_one(".js-c-india")
    return b.get_text(" ", strip=True) if b else "NA"


@lru_cache(maxsize=1)
def get_docs():
    soup, _ = get_soup(DOC_URL)
    rows = soup.select("table tbody tr")

    docs = []
    for r in rows:
        td = r.select_one("td")
        if not td:
            continue

        t = td.get_text(strip=True)

        if t and "checklist" not in t.lower():
            docs.append(t)

    return ", ".join(dict.fromkeys(docs)) if docs else "NA"


def get_fee(txt):
    m = re.search(r"£\s?\d{1,3}(?:,\d{3})+", txt)
    return m.group(0).replace(" ", "") if m else "NA"


def get_intake(txt):
    m = re.findall(r"\b(?:September|November|January|March|May|July)\s+\d{4}\b", txt)
    seen = []
    for x in m:
        if x not in seen:
            seen.append(x)
    return " ".join(sorted(seen)) if seen else "NA"


def get_ielts(txt):
    m = re.search(r"IELTS[^0-9]{0,50}(\d\.\d)", txt, re.I)
    return m.group(1) if m else "NA"


def get_boards(txt):
    m = re.search(r"boards only \((.*?)\)", txt, re.I)
    return m.group(1).strip() if m else "NA"


def get_waiver(txt):
    if "Standard XII English language" in txt:
        return "Available based on Class 12 English"
    return "NA"


def get_12th(txt):
    m = re.search(r"(60|65)%[^.]{0,50}(XII|12)", txt, re.I)
    return m.group(1) + "%" if m else "NA"


def get_grad(txt):
    m = re.search(r"(60|55)%[^.]{0,50}(degree|undergraduate)", txt, re.I)
    return m.group(1) + "%" if m else "NA"


def parse_course(u):
    soup, html = get_soup(u)
    txt = soup.get_text(" ", strip=True)

    name = get_dl(html, "courseName")
    lvl = get_dl(html, "levelOfStudy")
    camp = get_dl(html, "faculty")
    dur = get_dl(html, "studyMode")

    if name == "NA":
        h1 = soup.find("h1")
        name = h1.get_text(" ", strip=True) if h1 else "NA"

    if camp == "NA":
        loc = soup.select_one(".location")
        camp = loc.get_text(" ", strip=True) if loc else "NA"

    india = get_india()

    return {
        "program_course_name": name,
        "university_name": "Coventry University",
        "course_website_url": u,

        "campus": camp,
        "country": "UK",
        "address": "Coventry, UK",

        "study_level": lvl,
        "course_duration": dur,

        "all_intakes_available": get_intake(txt),

        "mandatory_documents_required": get_docs(),
        "yearly_tuition_fee": get_fee(txt),

        "scholarship_availability": "NA",
        "gre_gmat_mandatory_min_score": "NA",

        "indian_regional_institution_restrictions": "NA",

        "class_12_boards_accepted": get_boards(india),

        "gap_year_max_accepted": "NA",
        "min_duolingo": "NA",

        "english_waiver_class12": get_waiver(india),
        "english_waiver_moi": "NA",

        "min_ielts": get_ielts(india),

        "kaplan_test_of_english": "NA",
        "min_pte": "NA",
        "min_toefl": "NA",

        "ug_academic_min_gpa": get_grad(india) if "Postgraduate" in lvl else "NA",
        "twelfth_pass_min_cgpa": get_12th(india) if "Undergraduate" in lvl else "NA",

        "mandatory_work_exp": "NA",
        "max_backlogs": "NA",
    }