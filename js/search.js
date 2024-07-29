function loadGraphics() {
    // Hide container
    $('section.chart_container').hide();

    // Retrieve form value
    const peptide = $('#peptide_input').val();

    // Images and retrieval URLs.
    const images = [
        { id: '#heatmapImage', url: `./cgi-bin/generate_heatmap.cgi?peptide=${encodeURIComponent(peptide)}` },
        { id: '#correlationImage', url: `./cgi-bin/generate_corr_graph.cgi?peptide=${encodeURIComponent(peptide)}` }
    ];
    
    // Use promise chain to multithread image generation.
    Promise.all(images.map(img => 
        fetch(img.url)
            .then(response => response.blob())
            .then(blob => {
                const imgElement = $(img.id);
                imgElement.attr('src', URL.createObjectURL(blob));
                imgElement.show();
            })
        ))
        .then(() => {
            // Show the container once all images are loaded
            $('section.chart_container').show();
        })
        .catch(error => {
            alert('Error loading visualizations:', error);
        });
    }

// Get info about the protein from endpoint
function proteinInfo( term ) {
    // Hide the section
    $('section.protein_info').hide();

    // Retrieve form value
    const peptide = $('#peptide_input').val();

    // Get data from endpoint and process
    $.ajax({
        url: `./cgi-bin/get_protein_info.cgi?peptide=${peptide}`,
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            processProteinJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert(`${peptide} could not be found. Double check the spelling and try again.`);
        }
    });
}

// This processes a passed JSON structure representing protein info and 
// adds data to proper section of page.
function processProteinJSON( data ) {
    $('h3.peptide_target').text(data.peptide_target);
    $('span.gene_name').text(data.gene_name);
    $('span.summary').text(data.summary);
    $('span.location').text(data.location);

    // Show filled in section.
    $('section.protein_info').show();
}

// Run our javascript once the page is ready
$(document).ready( function() {
    // define what should happen when a user clicks submit on our search form
    $('#submit').click( function() {
        proteinInfo();
        loadGraphics();
        return false;  // prevents 'normal' form submission
    });
});
