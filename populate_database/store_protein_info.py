"""
Get info about each protein from Entrez and store in SQL db.
"""

import time
from Bio import Entrez
import re
import sqlite3

Entrez.email = "asmit397@jh.edu"

def create_protein_info_table(db_filename: str) -> None:
    """
    Create a table to hold info about each protein.
    """
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS protein_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peptide_target TEXT UNIQUE,
            name TEXT,
            summary FLOAT,
            location FLOAT
        )""")

        conn.commit()

def add_protein_info(peptide: str, info: tuple, db_filename: str) -> None:
    """
    Insert info about a protein into the table.
    """
    with sqlite3.connect(db_filename) as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO protein_info (peptide_target, name, summary, location)
            VALUES (?, ?, ?, ?)
            """, (peptide, *info))

            conn.commit()

        # If a row already exists for that protein, skip it.
        except sqlite3.IntegrityError:
            pass

def peptide_list(db_filename: str) -> list:
    """
    Retrieve a list of all peptides with expression data.
    """
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT DISTINCT peptide_target
        FROM expression_data
        WHERE protein_expression != 'NA'
        """,)

        peptides = cursor.fetchall()
        return [i[0] for i in peptides]

def missing_peptides(db_filename) -> list:
    """
    Retrieve a list of all peptides that don't have info stored yet.
    """
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT peptide_target
        FROM protein_info
        """,)

        peptides = cursor.fetchall()

    found = [i[0] for i in peptides]
    all = peptide_list(db_filename)
    return [i for i in all if i not in found]


def get_gene_info(protein_name):
    # Search for the protein in humans, sorting by relevance
    handle = Entrez.esearch(db="protein", term=f"{protein_name} AND human[Organism]", sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    time.sleep(0.5) # Rate limit Entrez calls

    # Return if nothing was found
    if not record["IdList"]:
        print(f"No protein found for: {protein_name}")
        return None

    # Get ID of most relevant protein
    protein_id = record["IdList"][0]

    # Fetch the protein record
    handle = Entrez.efetch(db="protein", id=protein_id, rettype="gb", retmode="text")
    protein_record = handle.read()
    handle.close()
    time.sleep(0.5) # Rate limit Entrez calls

    # Extract the GeneID from the protein record
    gene_id = None
    for line in protein_record.split('\n'):
        if '/gene=' in line.lower():
            pattern = r'"([^"]*)"'
            match = re.search(pattern, line)
            if match:
                gene_id = match.group(1)
            break

    # Return if nothing was found
    if not gene_id:
        print(f"No associated gene found for protein: {protein_name}")
        return None

    # Search for that gene in humans
    handle = Entrez.esearch(db="gene", term=f"{gene_id} AND {protein_name} AND human[Organism]", sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    time.sleep(0.5) # Rate limit Entrez calls

    # Return if nothing was found
    if not record["IdList"]:
        print(f"No gene found for: {gene_id}")
        return None

    # Get id of most relevant gene and retrieve summary
    gene_id = record["IdList"][0]
    handle = Entrez.esummary(db="gene", id=gene_id)
    summary = Entrez.read(handle)
    handle.close()

    # Return relevant information
    gene_info = summary['DocumentSummarySet']['DocumentSummary'][0]
    return gene_info.get('NomenclatureName'), gene_info.get('Summary'), gene_info.get('MapLocation')

def retrieve_store_from_entrez() -> None:
    """
    Get data from Entrez and store it in SQL db.
    """
    db_filename = 'protein_expression.db'
    create_protein_info_table(db_filename)

    # Get list of proteins we still need to look up
    protein_names = missing_peptides(db_filename)

    # Look up each one and store info in database
    for protein in protein_names:
        info = get_gene_info(protein)
        if info:
            print(info)
            add_protein_info(protein, info, db_filename)
        time.sleep(1)  # Keep this sleep between protein lookups

    # Make sure every protein is covered.
    still_missing = missing_peptides(db_filename)
    assert len(still_missing) == 0

if __name__ == "__main__":
    retrieve_store_from_entrez()
