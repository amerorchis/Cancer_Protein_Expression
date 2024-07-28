# Esophageal Cancer Protein Expression Explorer #
This project is for data exploration of a set of 125 esophageal cancer proteomes from the National Cancer Center.

Made by Andrew Smith for AS.410.712. Advanced Practical Computer Concepts for Bioinformatics.

## Features

- Search for expression data for different esophageal cancer proteins
- Get summary data about the protein and the gene that encodes it
- View a heatmap of the expression across the samples in the dataset

## Requirements

- Python 3
- The libraries contained in `requirements.txt`

Install the required library using pip:

```
pip install -r requirements.txt
```

## Installation and Usage

Clone the repository onto a device with a webserver. Place the CGI scripts into a directory where they can be executed. This is generally the cgi-bin directory in Apache configurations. Make sure they have executable permissions.

Access the main page at: `https://<domain>/path/to/main.html`, where `<domain>` is the root domain for your device (i.e. `http://bfx3.aap.jhu.edu`). 

Use the search box on the page to retrieve expression information about different proteins.
