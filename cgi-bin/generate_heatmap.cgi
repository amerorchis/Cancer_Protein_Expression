#!/usr/bin/env python3

import seaborn as sns
import numpy as np
import io
import sqlite3
from typing import List
import sys
import cgi
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from urllib.parse import unquote

def plot_expression_heatmap(expression_data: List[tuple], peptide: str, min_value: float=None, max_value: float=None) -> io.BytesIO:
    """
    Make a heatmap showing the expression level of the protein across samples.
    """
    # Make sure array is correct size
    assert len(expression_data) == 125

    # Convert to NP array
    expression_values = np.array([float(row[1]) for row in expression_data])

    # Reshape to 11x11 square with nub row at end
    matrix = np.full((12, 11), np.nan)
    matrix[:-1, :] = expression_values[:121].reshape(11, 11)
    matrix[-1, :4] = expression_values[121:]

    # Set up the matplotlib figure and draw heatmap
    fig, ax = plt.subplots(figsize=(6, 7))
    ax.set_title("Relative Expression Level Across Samples", fontsize=16)
    im = sns.heatmap(matrix, ax=ax, cmap='viridis', cbar=False, 
                     square=True, xticklabels=False, yticklabels=False,
                     vmin=min_value, vmax=max_value)

    # Create a new axes for the colorbar with the scale
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="5%", pad=0.1)
    cbar = plt.colorbar(im.get_children()[0], cax=cax, orientation="horizontal")
    cbar.outline.set_visible(False) # Hide colorbar outline

    ax.axis('off')
    plt.tight_layout()

    # Convert to buffer for CGI
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    return buf


def get_expression_data(peptide: str, db_filename: str) -> List[tuple]:
    """
    Get expression data for a given peptide across all samples.
    """
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT sample_id, protein_expression
        FROM expression_data
        WHERE peptide_target = ? COLLATE NOCASE
        """, (peptide,))

        return cursor.fetchall()

if __name__ == "__main__":
    MAX_EXPRESSION = 8.965824 # Highest value in entire table
    MIN_EXPRESSION = -4.377147 # Lowest value in entire table

    form = cgi.FieldStorage()
    encoded_peptide = form.getvalue('peptide')  # Get the encoded peptide name
    peptide = unquote(encoded_peptide)  # Decode the peptide name

    from db_path import db_filename
    expression_data = get_expression_data(peptide, db_filename)
    buf = plot_expression_heatmap(expression_data, peptide, min_value=MIN_EXPRESSION, max_value=MAX_EXPRESSION)

    # Write buffer rather than print for binary data
    sys.stdout.buffer.write(b"Content-Type: image/png\n\n")
    sys.stdout.buffer.write(buf.getvalue())
