import xml.etree.ElementTree as ET
import re  # ✅ For extracting emails using regex

def extract_email(root):
    """Extract email from multiple possible fields in the XML."""
    
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # ✅ Valid email format

    # ✅ 1. Check if email is inside <Affiliation>
    for aff in root.findall(".//Affiliation"):
        if aff is not None and aff.text:
            match = re.search(email_pattern, aff.text)
            if match:
                return match.group(0)  # ✅ Return first found email

    # ✅ 2. Check if email is inside <CommentsCorrections> (Corresponding Author)
    for comment in root.findall(".//CommentsCorrections"):
        if comment is not None and comment.text:
            match = re.search(email_pattern, comment.text)
            if match:
                return match.group(0)

    # ✅ 3. Check if email is inside <Correspondence>
    for corr in root.findall(".//Correspondence"):
        if corr is not None and corr.text:
            match = re.search(email_pattern, corr.text)
            if match:
                return match.group(0)

    return "N/A"  # ✅ Default if no email found

def extract_date(root):
    """Extract and format the publication date as YYYY-MM-DD."""
    
    # ✅ 1. Try extracting from <ArticleDate>
    year = root.findtext(".//ArticleDate/Year")
    month = root.findtext(".//ArticleDate/Month")
    day = root.findtext(".//ArticleDate/Day")

    if year:
        month = month if month else "01"  # Default to January if missing
        day = day if day else "01"  # Default to 1st if missing
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # ✅ 2. Try extracting from <DateCreated>
    year = root.findtext(".//DateCreated/Year")
    month = root.findtext(".//DateCreated/Month")
    day = root.findtext(".//DateCreated/Day")

    if year:
        month = month if month else "01"
        day = day if day else "01"
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # ✅ 3. Try extracting from <PubDate> (Fallback)
    pub_date = root.findtext(".//PubDate")
    if pub_date:
        return pub_date  # This might be in text format (e.g., "2024 Mar 7")

    return "N/A"  # ✅ Default if no date is found

def extract_relevant_data(raw_articles, debug: bool = False):
    """Extracts required fields from PubMed XML responses (better for affiliations & emails)."""
    
    results = []
    
    for xml_data in raw_articles:
        if not xml_data:
            continue

        root = ET.fromstring(xml_data)
        
        pubmed_id = root.findtext(".//ArticleId") or "N/A"
        title = root.findtext(".//ArticleTitle") or "N/A"
        pub_date = extract_date(root)  # ✅ Use the fixed date function
        corresponding_email = extract_email(root)  # ✅ Extract email correctly

        authors = []
        companies = []

        for author in root.findall(".//Author"):
            name = (
                author.findtext("LastName", default="") + " " + 
                author.findtext("ForeName", default="")
            ).strip()
            affiliation = author.findtext(".//Affiliation", default="N/A").strip()

            # ✅ Detect company affiliations
            company_keywords = ["inc", "ltd", "llc", "corporation", "biotech", "pharma", "gmbh", "s.a."]
            if any(word in affiliation.lower() for word in company_keywords):
                companies.append(affiliation)

            # ✅ Detect non-academic authors
            academic_keywords = ["university", "institute", "research", "college", "academy", "hospital"]
            if not any(word in affiliation.lower() for word in academic_keywords):
                authors.append(name)

        # ✅ Debugging: Print extracted values only in debug mode
        if debug:
            print(f"📌 PubMed ID: {pubmed_id}, Title: {title}, Date: {pub_date}")
            print(f"👤 Non-Academic Authors: {authors}")
            print(f"🏢 Companies: {companies}")
            print(f"📧 Corresponding Email: {corresponding_email}")

        results.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,  # ✅ Now in YYYY-MM-DD format
            "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
            "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
            "Corresponding Author Email": corresponding_email  # ✅ Now extracted correctly
        })
    
    return results
