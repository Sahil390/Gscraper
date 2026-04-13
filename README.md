# Coventry University Course Scraper

## About
This is a web scraping project built for the internship assignment.

It extracts course-related data from the official Coventry University website  
and stores it in JSON format.

Only 5 courses are scraped as per the assignment requirement.

---

## Tech Stack
- Python
- Requests
- BeautifulSoup (bs4)
- lxml

---

## Project Structure

- scraper/
  - crowler.py  → fetches course links
  - parser.py   → extracts data from each course page
- main.py       → runs the scraper
- output/
  - data.json   → final output file

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 lxml
```

---

## How to Run

```bash
python main.py
```

---

## Output

- Output file: `output/data.json`
- Contains data for 5 courses
- Follows the schema given in the assignment

---

## Notes

- Data is scraped only from the official Coventry University website
- No hardcoded values are used
- Missing fields are handled as `"NA"`
- Raw text is used where needed instead of over-processing
- Handles different page structures like:
  - multiple course durations
  - fees tables
  - international entry requirements page

---

## Limitations

- Some fields contain raw text instead of perfectly formatted values
- Intake and duration format may vary depending on the course page
- Scraper is limited to 5 courses (as required)

---

## Author

Sahil Narang