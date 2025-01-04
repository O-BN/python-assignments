'''
Parameters:
    --database: NCBI database to search
    --term: Search term
    --number: Number of items to download (default: 10)
    --organism: Filter results by species (default: mus musculus)

NCBI datebase: 
    --"pubmed", "protein", "nuccore", "nucleotide", "gene", "genome", "structure", "taxonomy", "snp", "dbvar", "biosample", "bioproject"
'''

# Importing required libraries
import argparse
import csv
import os
import time
from Bio import Entrez

# Set your email for NCBI Entrez API access
Entrez.email = "your_email@example.com" # Change this to your email

###Search the NCBI database and return the results.###
def search_ncbi(database, term, number, organism):
    query = f"{term} [ORGANISM:{organism}]"
    handle = Entrez.esearch(db=database, term=term, retmax=number)
    record = Entrez.read(handle)
    handle.close()
    return record

    ###Fetch records from NCBI database given a list of IDs.###
def fetch_records(database, ids):

    handle = Entrez.efetch(db=database, id=ids, rettype="gb", retmode="text")
    return handle.read()

###Save the content to a file.###
def save_record(file_name, content):

    with open(file_name, "w") as file:
        file.write(content)

###Record the search details to a CSV file.###
def record_search_to_csv(file_name, date, database, organism, term, max_number, total):

    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["date", "database", "organism", "term", "max", "total"])
        writer.writerow([date, database, organism, term, max_number, total])

###Main function to run the script.###
def main():
    #Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download data from NCBI.")
    parser.add_argument("--database", type=str, default="protein", help="NCBI database to search")
    parser.add_argument("--term", type=str, required=True, help="Search term")
    parser.add_argument("--number", type=int, default=10, help="Number of items to download")
    parser.add_argument("--organism", type=str, default="mus musculus", help="Filter results by organism (default: mus musculus)")
    args = parser.parse_args()

    # Define an output directory for the downloaded records
    output_directory = "downloaded_records"
    
    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    #Search NCBI
    print(f"Searching NCBI {args.database} database for term '{args.term}' with organism '{args.organism}'...")
    try:
        search_results = search_ncbi(args.database, args.term, args.number, args.organism)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    total_results = int(search_results["Count"])
    ids = search_results["IdList"]

    print(f"Found {total_results} results. Downloading up to {len(ids)} items...")

    #Fetch and save records
    for index, record_id in enumerate(ids):
        content = fetch_records(args.database, record_id)
        file_name = os.path.join(output_directory, f"{args.term.replace(' ', '_')}_{index + 1}.txt")
        save_record(file_name, content)
        print(f"Saved: {file_name}")

    #Record search details
    searches_file = "searches_history.csv"
    record_search_to_csv(searches_file, time.strftime("%Y-%m-%d %H:%M:%S"),  args.database, args.organism, args.term, args.number, total_results)
    print(f"Search logged to {searches_file}")

if __name__ == "__main__":
    main()
