# Importing required libraries
from flask import Flask, request, render_template, jsonify, send_file
import os
import time
import csv
from Bio import Entrez

'''
Parameters:
    --database: NCBI database to search
    --term: Search term
    --number: Number of items to download (default: 10)
    --organism: Filter results by species (default: mus musculus)

NCBI datebase: 
    --"pubmed", "protein", "nuccore", "nucleotide", "gene", "genome", "structure", "taxonomy", "snp", "dbvar", "biosample", "bioproject"
'''

app = Flask(__name__)

# Set your email for NCBI Entrez API access
Entrez.email = "osherbenun@gmail.com"  # Change this to your email


###Search the NCBI database and return the results.###
def search_ncbi(database, term, number, organism):
    query = f"{term} AND {organism}[ORGN]"
    try:
        handle = Entrez.esearch(db=database, term=query, retmax=number)
        record = Entrez.read(handle)
        handle.close()
        return record
    except Exception as e:
        print(f"Error in search_ncbi: {e}")
        return {"Count": "0", "IdList": []}  # Return empty result on failure


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


# Define an output directory for the downloaded files
output_directory = "downloaded_files"

# Create the directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Define an output directory for the downloaded files
searches_file = "searches_history.csv"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        database = request.form.get("database", "protein")
        term = request.form.get("term")
        number = int(request.form.get("number", 10))
        organism = request.form.get("organism", "mus musculus")

        if not term:
            return render_template("index.html", error="Search term is required!")

        # Search NCBI
        try:
            search_results = search_ncbi(database, term, number, organism)
            total_results = int(search_results["Count"])

            if total_results == 0:
                return render_template(
                    "index.html", error=f"No results found for query: {term} in {organism}."
                )

            ids = search_results["IdList"]
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")


        # Fetch and save records
        saved_files = []
        for index, record_id in enumerate(ids):
            content = fetch_records(database, record_id)
            file_name = os.path.join(output_directory, f"{term.replace(' ', '_')}_{index + 1}.txt")
            save_record(file_name, content)
            saved_files.append(file_name)

        # Record search details
        record_search_to_csv(searches_file, time.strftime("%Y-%m-%d %H:%M:%S"), database, organism, term, number, total_results)

        return render_template("index.html", saved_files=saved_files, total_results=total_results)

    return render_template("index.html")


### Web interface: Serve downloaded files ###
@app.route("/download/<filename>")
def download_file(filename):
    """Serve a downloaded file."""
    file_path = os.path.join(output_directory, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404


### Web interface: Serve the log file ###
@app.route("/download_log")
def download_log():
    """Serve the search log file."""
    if os.path.exists(searches_file):
        return send_file(searches_file, as_attachment=True)
    return "Log file not found", 404

### Run the Flask application ###
if __name__ == "__main__":
    app.run(debug=True)
