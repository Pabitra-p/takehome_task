# PubMed Scraper

## 📖 Description
A command-line tool to fetch and filter research papers from PubMed, focusing on papers with at least one author affiliated with a pharmaceutical or biotech company.

## 🚀 Features
- Fetches PubMed research papers using the PubMed API.
- Filters papers to identify **non-academic authors** and **company affiliations**.
- Saves results as a CSV file with relevant details.
- Provides a command-line interface with options for **debugging** and **file output**.

## 📦 Installation

### 1️⃣ Install Poetry (If Not Installed)
```sh
curl -sSL https://install.python-poetry.org | python3 -


##To get results
poetry install
poetry run get-papers-list "cancer research" -f results.csv

### **Command-line Options**
- `-h, --help` : Show usage instructions.
- `-d, --debug` : Enable debug mode.
- `-f, --file <filename>` : Save results to a CSV file.

