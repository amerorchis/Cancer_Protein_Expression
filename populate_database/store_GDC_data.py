"""
Store the National Cancer Institute GDC Data Portal data in a SQL database.
"""

import sqlite3
from typing import NamedTuple, List

class ExpLevel(NamedTuple):
# Define a data structure for a single expression level data point.
    id: str
    AGID: str
    lab_id: int
    catalog_number: str
    set_id: str
    peptide_target: str
    protein_expression: float

def build_table(db_filename: str) -> None:
    """
    Create a table to store expression level data.
    """

    with sqlite3.connect(db_filename) as conn:
        curs = conn.cursor()

        curs.execute("""
        CREATE TABLE IF NOT EXISTS expression_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            AGID TEXT,
            lab_id INT,
            catalog_number TEXT,
            set_id TEXT,
            peptide_target TEXT,
            protein_expression FLOAT
        )
        """)

        conn.commit()

def process_file(filename: str, _id: str) -> List[ExpLevel]:
    """
    Take a given csv file and parse the data into a list of ExpLevel objects.
    """
    with open(filename, 'r') as f:
        raw = f.read()

    samples = raw.split('\n')[1:]
    return [ExpLevel(_id, *i.split('\t')) for i in samples if i]

def add_expression_to_db(exp_level: ExpLevel, db_filename: str) -> None:
    """
    Add a ExpLevel object as a row in the table.
    """
    with sqlite3.connect(db_filename) as conn:
        curs = conn.cursor()

        curs.execute("""
        INSERT INTO expression_data
        (sample_id, AGID, lab_id, catalog_number, set_id, peptide_target, protein_expression)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (exp_level.id, exp_level.AGID, exp_level.lab_id, exp_level.catalog_number, 
              exp_level.set_id, exp_level.peptide_target, exp_level.protein_expression))

        conn.commit()

def process_manifest() -> list:
    """
    Open a GDC manifest file, parse info about the data files, and store the data in a database.
    """

    # Make a list of files described in the manifest.
    manifest = 'GDC Data/gdc_manifest.2024-07-09.txt'
    with open(manifest, 'r') as f:
        man = f.read()
    files = man.split('\n')[1:]
    files = [i.split('\t') for i in files if i]

    # For each file, extract data, then store data in database.
    for sample in files:
        _id = sample[0]
        filename = f'GDC Data/{_id}/{sample[1]}'
        expression_levels = process_file(filename, _id)
        for exp_level in expression_levels:
            add_expression_to_db(exp_level, 'protein_expression.db')

if __name__ == "__main__":
    build_table('protein_expression.db')
    process_manifest()
