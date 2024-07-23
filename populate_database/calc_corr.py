"""
Calculate PCC for each possible protein pairing and record in a table.
"""


import sqlite3
import pandas as pd
from itertools import combinations_with_replacement

def calc_correlations(db_filename: str) -> pd.DataFrame:
    # Get all expression level points
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT peptide_target, sample_id, protein_expression
        FROM expression_data
        """)
        data = cursor.fetchall()

    # Pivot DF to make each row a sample and each column a peptide
    df = pd.DataFrame(data, columns=['peptide', 'sample_id', 'protein_expression'])
    pivot_df = df.pivot(index='sample_id', columns='peptide', values='protein_expression')

    # Convert expression level strings to floats.
    pivot_df = pivot_df.apply(pd.to_numeric, errors='coerce')
    pivot_df = pivot_df.dropna(axis=1) # A few proteins have no expression recorded, drop them.

    # Make sure no NaNs are left
    na_counts = pivot_df.isna().sum()
    na_counts = na_counts[na_counts > 0]
    assert len(na_counts) == 0

    # Return correlations
    return pivot_df.corr()


def create_correlations_table(db_filename: str) -> None:
    """
    Create a table in the database to store correlation data.
    """

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expression_correlations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peptide1 TEXT,
            peptide2 TEXT,
            correlation FLOAT,
            absolute_correlation FLOAT,
            UNIQUE(peptide1, peptide2)
        )""")

        conn.commit()

def insert_correlations(corrs: pd.DataFrame, db_filename: str) -> None:
    """
    Take the correlations DF and store each value in the SQL table.
    """

    corr_data = []
    peptides = corrs.columns.to_list()

    # Iterate through each pairing of peptides
    for t1, t2 in combinations_with_replacement(peptides, 2):
        # Add correlation between them to the table (with each one in slot 1 and 2).
        corr = corrs.loc[t1, t2]
        corr_data.append((t1, t2, corr, abs(corr)))
        if t1 != t2:
            corr_data.append((t2, t1, corr, abs(corr)))

    # Add each of these correlations to the db.
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.executemany("""
        INSERT INTO expression_correlations (peptide1, peptide2, correlation, absolute_correlation)
        VALUES (?, ?, ?, ?)
        """, corr_data)

        conn.commit()

if __name__ == "__main__":
    db_filename = 'protein_expression.db'
    create_correlations_table(db_filename)
    corrs = calc_correlations(db_filename)
    insert_correlations(corrs, db_filename)
