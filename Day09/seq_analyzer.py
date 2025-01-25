# Importing required libraries
import os
import re
import csv
import argparse
from Bio import Entrez, SeqIO

# Set your email for NCBI Entrez API access
Entrez.email = "your_email@example.com"  # Change this to your email

# Validate the file format (FASTA or GenBank)
def validate_file_format(file_path):
    valid_extensions = [".fa", ".gb", ".gbk"]
    if not any(file_path.endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Invalid file format for {file_path}. Supported formats are: FASTA and GenBank.")

# Find the longest repeated subsequence in a string
def find_longest_repeated_subsequence(sequence):
    n = len(sequence)
    lcs_table = [[0] * (n + 1) for _ in range(n + 1)]
    longest = ""
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if sequence[i - 1] == sequence[j - 1] and lcs_table[i - 1][j - 1] < (j - i):
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
                if lcs_table[i][j] > len(longest):
                    longest = sequence[i - lcs_table[i][j]:i]
            else:
                lcs_table[i][j] = 0
    return longest

# Calculate GC percentage for a given sequence
def calculate_gc_percentage(sequence):
    gc_count = sequence.count("GC")
    return (gc_count / len(sequence)) * 100

# Download files from NCBI if not found
def download_files(database, term, organism, number, output_directory):
    print(f"Downloading {number} records for term '{term}' from {database} database...")
    search_results = Entrez.esearch(db=database, term=term, retmax=number)
    record = Entrez.read(search_results)
    ids = record["IdList"]

    for index, record_id in enumerate(ids):
        handle = Entrez.efetch(db=database, id=record_id, rettype="FASTA", retmode="text")
        content = handle.read()
        file_name = os.path.join(output_directory, f"{term.replace(' ', '_')}_{database}_{organism.replace(" ", "_")}_{index + 1}.fa")
        with open(file_name, "w") as file:
            file.write(content)
        print(f"Downloaded and saved: {file_name}")

# Analyze only matching downloaded files
def analyze_files(output_directory, duplicate_analysis, gc_analysis, term, database, organism):
    results = []
    # Sanitize inputs for matching filenames
    term_sanitized = term.replace(" ", "_").lower()
    database_sanitized = database.lower()
    organism_sanitized = organism.replace(" ", "_").lower()

    # Filter files based on term, database, and organism
    files = [
        f for f in os.listdir(output_directory)
        if f.endswith((".fa", ".gb", ".gbk"))
        and term_sanitized in f.lower()
        and database_sanitized in f.lower()
        and organism_sanitized in f.lower()
    ]

    # Proceed with the analysis if matches are found
    print("Analyzing files...")
    for file in files:
        file_path = os.path.join(output_directory, file)
        try:
            validate_file_format(file_path)
            with open(file_path, "r") as handle:

                # Read the sequence in the appropriate format
                record = SeqIO.read(handle, format="genbank" if file.endswith(".gb") else "fasta")
                sequence = str(record.seq)

                # Perform analyses
                longest_subseq = find_longest_repeated_subsequence(sequence) if duplicate_analysis else None
                gc_percentage = calculate_gc_percentage(sequence) if gc_analysis else None

                # Append results
                results.append((file, len(longest_subseq) if longest_subseq else 0, longest_subseq or "N/A", gc_percentage if gc_percentage is not None else "N/A"))
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Print and save results
    sanitized_term = term.replace(" ", "_")  # Replace spaces with underscores
    summary_file = os.path.join(output_directory, f"analysis_summary_{sanitized_term}_{database_sanitized}_{organism_sanitized}.csv")
    with open(summary_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Longest Repeated Subsequence Length", "Subsequence", "GC Percentage"])
        for result in results:
            writer.writerow(result)
            print(f"File: {result[0]}, Longest Subsequence Length: {result[1]}, Subsequence: {result[2]}, GC%: {round(float(result[3]), 2) if isinstance(result[3], (int, float)) else result[3]}")

    print(f"Analysis summary saved to {summary_file}")


# Main function
def main():
    parser = argparse.ArgumentParser(description="Analyze NCBI downloaded files for repeated subsequences and GC content.")
    parser.add_argument("--database", type=str, default="nucleotide", help="NCBI database to search")
    parser.add_argument("--term", type=str, required=True, help="Search term")
    parser.add_argument("--number", type=int, default=10, help="Number of items to download")
    parser.add_argument("--organism", type=str, default="mus musculus", help="Filter results by organism")
    parser.add_argument("--duplicate", action="store_true", help="Analyze for the longest repeated subsequence")
    parser.add_argument("--gc", action="store_true", help="Analyze GC percentage for the sequence with the longest repeated subsequence")
    args = parser.parse_args()

    # Set up output directory
    output_directory = "downloaded_records"
    os.makedirs(output_directory, exist_ok=True)

    # Ensure files are available
    files = [f for f in os.listdir(output_directory) 
            if f.endswith((".fa", ".fa", ".gb", ".gbk")) and args.term.replace(" ", "_").lower() and args.database in f.lower()]
    if not files:
        download_files(args.database, args.term, args.organism, args.number, output_directory)

    # Perform analyses
    if args.duplicate or args.gc:
        analyze_files(output_directory, args.duplicate, args.gc, args.term, args.database, args.organism)
    else:
        print("No analysis selected. Use --duplicate or --gc to perform an analysis.")

if __name__ == "__main__":
    main()
