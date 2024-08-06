# Esophageal Cancer Protein Expression Explorer

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

Clone the repository onto a device configured as a webserver. Place the CGI scripts into a directory where they can be executed. This is generally the cgi-bin directory in Apache configurations. Make sure they have executable permissions.

Access the main page at: `https://<domain>/path/to/main.html`, where `<domain>` is the root domain for your device (i.e. `http://bfx3.aap.jhu.edu`).

On the class server, the project can be found at [http://bfx3.aap.jhu.edu/asmit397/final/main.html](http://bfx3.aap.jhu.edu/asmit397/final/main.html).

Use the search box on the page to retrieve expression information about different proteins.

## Functionality

This tool is a webpage with a search bar. Users can type of the name of any of the 455 proteins in the database, then submit the form by clicking the button to get information about their chosen protein. For example, searching `HER2` will retrieve information about the receptor tyrosine-protein kinase erbB-2 protein. Upon form submission, the protein name is sent to three endpoints, which return: information about the protein and the gene that encodes it, a graph showing the 10 other proteins with the most significant correlation in expression levels to the chosen protein, and a heatmap showing the expression level in each of the 125 samples in the dataset. The page gives the user important information to try to understand the function of a given protein, its connection to different regulatory or metabolic pathways, if it is up or down regulated in the cancer samples, and how much variance there is in expression between individuals. The goal of the tool is to identify potentially important protein markers in esophageal cancer, how these proteins interact with other proteins, and eventually to identify potential drug targets.

### **Description of Features**

This site uses all the major technique that we have studied this term in order to create a cohesive product.

1. HTML: The user is first presented with an HTML5 page, which uses semantic rather than presentational markup. The page has a clean appearance and initially only shows a heading, some background information on the project, and a simple search form. Results are contained in hidden sections that appear when they are populated. Styling is separated to CSS and interactive content separated to a JavaScript file that are linked in the header of the HTML file. The boilerplate template is used to start the page with the critical elements.
2. CSS: A CSS stylesheet is used to style the document, with selectors that target the desired elements using tags, classes, and ids. The new flexbox column design capabilities of HTML5 are used to control the layout of the visualizations, allowing each to be as large as possible while staying in the correct size and position relative to each other and the rest of the page. The wider correlation graph takes up 2/3 of the row and the more vertical heatmap uses the remaining 1/3 with an appropriate amount of padding between. The background gradient is based on the color for esophageal cancer, purple. The favicon is an amerorchis flower, which I like to include in all of my work.
3. JavaScript: There are two JavaScript files linked from the HTML. One makes a call to the autocomplete CGI endpoint to populate the jQuery autocomplete element in the search form. The other script is triggered by a search, and retrieves information about the protein, as well as the two graphs. The information is received in JSON format, then used to set the values of the correct HTML elements. CGI endpoints are called using AJAX.
4. Python CGI: There are three Python CGI scripts that handle requests from the JS scripts. The autocomplete script returns a list of valid search terms for the search form, and each of the visualizations has a script that generates graphs in matplot lib and returns the encoded image files. Each of the python scripts works in generally the same way: it accepts a protein name argument from the search form (except the autocomplete one, which always uses the same parameters), opens a connection and makes a SQL query, processes the data, converts data to JSON format, and returns it to the calling function.
5. Relational databases: Although the data originates on NCBI sites, I have downloaded it and stored it in a sqlite relational database. Sqlite was chosen over mySQL simply because it allowed for me to work on the project offline. There are a few advantages to storing the data locally, rather than accessing it on NCBI sites. This reduces API calls to Entrez, which are slow and which strain resources that are shared between many researchers. It also allows the data to be normalized and stored in a relational way that makes the connection between different datasets clear. It also allows me to cache computationally expensive operations for quick access. The disadvantage is that if data is updated on NCBI servers, this will not be reflected on the site. There are three table which store metadata about each protein, expression levels for each sample, and correlations between each protein pairing.
6. Markdown: This readme file was created using Markdown. The document gives information about the installation and use of the program. Markdown is used to style the document to present the information in a clearer and more organized way.
