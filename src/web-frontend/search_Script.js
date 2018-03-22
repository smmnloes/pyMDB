var results = $('#search_results');

function make_query() {
    var director = $('#director_input').value;
    var writer = $('#writer_input').value;
    var year_from = $('#year_from_input');
    var year_to = $('#year_to_input');
    var genres = $('#genres_input');
    var minRatingIMDB = $('#minRatingIMDB_input');

    var requestBody = {
        "director": director,
        "writer": writer,
        "year_from": year_from,
        "year_to": year_to,
        "genres": genres,
        "minRatingIMDB": minRatingIMDB
    };


    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://localhost:5002/query", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    xhttp.send(JSON.stringify(requestBody));
    var response = JSON.parse(xhttp.responseText);
    $('#results_span').value = response;
}
