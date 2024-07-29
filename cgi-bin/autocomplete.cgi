#!/usr/bin/env python3

import json
import sqlite3

from db_path import db_filename

def main(db_filename: str) -> None:
    """
    Return a list of all peptide targets with data available
    """

    print("Content-Type: application/json\n\n")

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT DISTINCT peptide_target
        FROM expression_data
        WHERE protein_expression != 'NA'
        """,)

        peptides = cursor.fetchall()
        peptides = [i[0] for i in peptides]

    # Print in JSON format
    print(json.dumps({ 'products' : peptides }))


if __name__ == '__main__':
    main(db_filename)
