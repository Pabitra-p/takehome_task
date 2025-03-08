import argparse
import pandas as pd
from pubmed_scrapper.fetcher import fetch_pubmed_data
from pubmed_scrapper.parser import extract_relevant_data

def main():
    # Create CLI argument parser
    parser = argparse.ArgumentParser(
        description="Fetch and filter PubMed papers with at least one non-academic author."
    )

    # Required argument: Query for PubMed
    parser.add_argument("query", type=str, help="Search query for PubMed articles.")

    # Optional: Output file
    parser.add_argument(
        "-f", "--file", type=str, help="Filename to save results as CSV. If not provided, prints output to console."
    )

    # Optional: Enable debugging mode
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode to show API requests and processing details."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Fetch raw data from PubMed API
    raw_data = fetch_pubmed_data(args.query, debug=args.debug)

    # ✅ Handle empty results
    if not raw_data:
        print("❌ No results found. Try a different query.")
        return  # Exit gracefully

    # Process & filter results
    processed_data = extract_relevant_data(raw_data, debug=args.debug)  # ✅ Pass debug flag

    # Output results
    if args.file:
        df = pd.DataFrame(processed_data)
        df.to_csv(args.file, index=False)
        print(f"✅ Results saved to {args.file}")
    else:
        print("\n✅ Processed Results:")
        for paper in processed_data:
            print(f"📌 {paper['Title']}")
            print(f"   🆔 PubMed ID: {paper['PubmedID']}")
            print(f"   📅 Date: {paper['Publication Date']}")
            print(f"   👤 Non-Academic Authors: {paper['Non-academic Author(s)']}")
            print(f"   🏢 Companies: {paper['Company Affiliation(s)']}")
            print(f"   📧 Email: {paper['Corresponding Author Email']}")
            print("-" * 80)  # Separator for readability

if __name__ == "__main__":
    main()
