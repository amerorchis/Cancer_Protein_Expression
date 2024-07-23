#!/usr/local/bin/python3

import json
import sqlite3

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
    db_filename = 'protein_expression.db'
    main(db_filename)
