import re
import requests
from bs4 import BeautifulSoup
from functools import lru_cache

BASE = "https://www.coventry.ac.uk/international-students-hub/entry-requirements/"
sess = requests.Session()


def get_soup(u):
    r = sess.get(u, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml"), r.text


def get_dl_val(html, key):
    pats = [
        rf"'{re.escape(key)}'\s*:\s*'([^']*)'",
        rf'"{re.escape(key)}"\s*:\s*"([^"]*)"',
    ]
    for p in pats:
        m = re.search(p, html, re.DOTALL)
        if m:
            return m.group(1).strip()
    return "NA"


@lru_cache(maxsize=1)
def get_india():
    soup, _ = get_soup(BASE)
    b = soup.select_one(".js-c-india")
    return b if b else None


def get_sec(b, name):
    if not b:
        return "NA"

    h = b.find("h3", string=re.compile(rf"^{re.escape(name)}$", re.I))
    if not h:
        return "NA"

    out = []
    for s in h.find_next_siblings():
        if s.name == "h3":
            break
        t = s.get_text(" ", strip=True)
        if t:
            out.append(t)

    return " ".join(out) if out else "NA"


def get_fee(txt):
    m = re.search(r"£\s?\d{1,3}(?:,\d{3})+", txt)
    return m.group(0).replace(" ", "") if m else "NA"


def get_intake(txt):
    m = re.findall(r"\b(?:September|November|January|March|May|July)\s+\d{4}\b", txt)
    seen = []
    for x in m:
        if x not in seen:
            seen.append(x)
    return " ".join(seen[:6]) if seen else "NA"


def find_pct(txt, keys, w=200):
    low = txt.lower()

    for k in keys:
        for m in re.finditer(re.escape(k.lower()), low):
            s = max(0, m.start() - w)
            e = min(len(txt), m.end() + w)

            chunk = txt[s:e]
            p = re.search(r"\b\d{1,2}(?:\.\d)?%", chunk)

            if p:
                return p.group(0)

    return "NA"


def get_ielts(txt):
    m = re.search(r"IELTS[^0-9]{0,50}(\d\.\d)", txt, re.I)
    return m.group(1) if m else "NA"


def get_boards(txt):
    m = re.search(r"boards only \((.*?)\)", txt, re.I)
    return m.group(1).strip() if m else "NA"


def get_waiver(txt):
    if "Standard XII English language" in txt:
        return "Available based on Class 12 English marks"
    return "NA"


def get_gpa(txt, lvl):
    if txt == "NA":
        return "NA"

    if "Postgraduate" in lvl:
        return find_pct(txt, ["undergraduate degree", "three year", "four year"])

    return find_pct(txt, ["standard xii", "class 12", "12th"])


def parse_course(u):
    soup, html = get_soup(u)
    txt = soup.get_text(" ", strip=True)

    name = get_dl_val(html, "courseName")
    lvl = get_dl_val(html, "levelOfStudy")
    camp = get_dl_val(html, "faculty")
    dur = get_dl_val(html, "studyMode")

    if name == "NA":
        h1 = soup.find("h1")
        name = h1.get_text(" ", strip=True) if h1 else "NA"

    if camp == "NA":
        loc = soup.select_one(".location")
        camp = loc.get_text(" ", strip=True) if loc else "NA"

    india = get_india()
    ug = get_sec(india, "Undergraduate")
    pg = get_sec(india, "Postgraduate")

    sec = pg if "Postgraduate" in lvl else ug

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

        "mandatory_documents_required": "NA",
        "yearly_tuition_fee": get_fee(txt),

        "scholarship_availability": "NA",
        "gre_gmat_mandatory_min_score": "NA",

        "indian_regional_institution_restrictions": "NA",

        "class_12_boards_accepted": get_boards(sec),

        "gap_year_max_accepted": "NA",
        "min_duolingo": "NA",

        "english_waiver_class12": get_waiver(sec),
        "english_waiver_moi": "NA",

        "min_ielts": get_ielts(sec),

        "kaplan_test_of_english": "NA",
        "min_pte": "NA",
        "min_toefl": "NA",

        "ug_academic_min_gpa": get_gpa(sec, lvl),

        "twelfth_pass_min_cgpa": "NA",
        "mandatory_work_exp": "NA",
        "max_backlogs": "NA",
    }