// Declare autocompleteOptions
var autocompleteOptions = [];

// this function gets autocomplete options via an AJAX call
function getAutocompleteOptions() {
    $.ajax({
        url: './cgi-bin/autocomplete.py',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            autocompleteOptions = data.products || []; // Get products list or an empty array.
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to get autocomplete options! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

// run our javascript once the page is ready
$(document).ready( function() {

    // Set autocompleteOptions with current options
    getAutocompleteOptions()

    $("#peptide_input").autocomplete({
        source: function(request, response) {

            // Filter based on the term and return 5
            var results = $.ui.autocomplete.filter(autocompleteOptions, request.term);
            response(results.slice(0,5));
        },
        minLength: 0
    });
});
