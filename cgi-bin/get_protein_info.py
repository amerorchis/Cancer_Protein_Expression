#!/usr/local/bin/python3

import json
import sqlite3
from typing import List
import cgi
from urllib.parse import unquote

def get_protein_info(peptide: str, db_filename: str) -> List[tuple]:
    """
    Get and JSONify info about the peptide_target.
    """

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT peptide_target, name, summary, location
        FROM protein_info
        WHERE peptide_target = ? COLLATE NOCASE
        """, (peptide,))

        data = cursor.fetchone()

    # Print in JSON format
    print("Content-Type: application/json\n\n")
    print(json.dumps({
        'peptide_target' : data[0],
        'gene_name' : data[1],
        'summary' : data[2],
        'location' : data[3],
    }))

if __name__ == "__main__":
    db_filename = 'protein_expression.db'
    form = cgi.FieldStorage()
    encoded_peptide = form.getvalue('peptide')  # Get the encoded peptide name
    peptide = unquote(encoded_peptide)  # Decode the peptide name

    get_protein_info(peptide, db_filename)
