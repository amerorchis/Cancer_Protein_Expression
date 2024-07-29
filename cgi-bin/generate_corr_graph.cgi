#!/usr/bin/env python3

import cgi
import sys
import io
import sqlite3
from urllib.parse import unquote
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd


def get_protein_correlations(db_filename: str, target_protein: str, limit=10) -> Tuple[str, pd.DataFrame]:
    """
    Retrieve protein correlation data from the database.
    """
    with sqlite3.connect(db_filename) as conn:

        cursor = conn.cursor()
        # Get proper capitalization for peptide name
        cursor = conn.cursor()
        cursor.execute("""
            SELECT peptide_target
            FROM protein_info
            WHERE peptide_target = ? COLLATE NOCASE
            """, (target_protein,))
        target_protein = cursor.fetchone()[0]
        cursor.close()

        # Find the <limit> peptides with highest absolute correlation
        query = """
        SELECT peptide2, correlation
        FROM expression_correlations
        WHERE peptide1 = ? AND peptide2 != ?
        ORDER BY absolute_correlation DESC
        LIMIT ?
        """

        # Store results in pandas dataframe
        df = pd.read_sql_query(query, conn, params=(target_protein, target_protein, limit))

    # Sort by actual correlation
    return target_protein, df.sort_values('correlation')

def plot_protein_correlations(df, target_protein):
    """
    Plot protein correlations as a horizontal bar chart.
    """

    plt.figure(figsize=(12, 8))

    # Bar for each protein
    bars = plt.barh(range(len(df)), df['correlation'])

    # Chart styling
    plt.title(f"Most Significant Protein Expression Correlations with {target_protein}", fontsize=16)
    plt.axis('off')
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)

    # Set color based on if correlation is positive or negative
    for bar in bars:
        bar.set_color('red' if bar.get_width() < 0 else 'green')

    # Add label with protein name and correlation value
    for i, (protein, correlation) in enumerate(zip(df['peptide2'], df['correlation'])):

        # Add protein name on the bar
        x_pos = correlation / 2
        plt.text(x_pos, i, protein, va='center', ha='center', fontweight='bold', color='white')

        # Add correlation value outside the bar
        if correlation < 0: # Negative values on left
            plt.text(correlation - 0.01, i, f'{correlation:.3f}', va='center', ha='right', fontweight='bold')
        else: # Positive values on right
            plt.text(correlation + 0.01, i, f'{correlation:.3f}', va='center', ha='left', fontweight='bold')

    plt.tight_layout()

    # Convert to buffer for CGI
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    return buf

if __name__ == "__main__":
    form = cgi.FieldStorage()
    encoded_peptide = form.getvalue('peptide')  # Get the encoded peptide name
    peptide = unquote(encoded_peptide)  # Decode the peptide name

    from db_path import db_filename

    peptide, df = get_protein_correlations(db_filename, peptide)
    buf = plot_protein_correlations(df, peptide)

    # Write buffer rather than print for binary data
    sys.stdout.buffer.write(b"Content-Type: image/png\n\n")
    sys.stdout.buffer.write(buf.getvalue())
