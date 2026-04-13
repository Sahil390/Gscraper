# Coventry University Scraper

## about
this is a simple web scraping project i made for the assignment

it scrapes course data from the official coventry university website  
and stores it in json format

only 5 courses are scraped as required

---

## tech used
- python
- requests
- beautifulsoup (bs4)
- lxml

---

## project structure

scraper/
- crowler.py -> gets course links  
- parser.py -> extracts data from course pages  

main.py -> runs everything  
output/
- data.json -> final output  

---

## setup

install dependencies:

pip install -r requirements.txt

or manually:

pip install requests beautifulsoup4 lxml

---

## run

python main.py

---

## output

- file: output/data.json  
- contains 5 course data  
- follows given schema  

---

## notes

- data is scraped only from official coventry site  
- no hardcoding of values  
- if data is missing -> "NA"  
- raw text is used wherever needed (no over cleaning)  
- handled different page structures like:
  - multiple duration formats  
  - international requirements page  
  - fees table  

---

## limitations

- some fields are raw text (not perfectly formatted)
- intake and duration format may vary depending on course
- scraper is made for 5 courses only (as per assignment)

---

## author

sahil narang
