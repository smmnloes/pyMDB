function make_query() {
    var director = $('#director_input').val();
    var writer = $('#writer_input').val();
    var year_from = parseInt($('#year_from_input').val());
    var year_to = parseInt($('#year_to_input').val());
    var genres = $('#genres_input').val();
    var minRatingIMDB = parseFloat($('#minRatingIMDB_input').val());
    var principals = $('#principals_input').val();
    var search_results = $('#results_list');
    var result_size = $('#result_size');

    search_results.empty();

    var requestBody = {
        "director": director,
        "writer": writer,
        "year_from": year_from,
        "year_to": year_to,
        "genres": (genres === '') ? null : genres.split(','),
        "minRatingIMDB": minRatingIMDB,
        "principals": (principals === '') ? null : principals.split(',')
    };

    var requestJson = JSON.stringify(requestBody);
    console.log(requestJson);

    $.ajax({
        url: "http://localhost:5002/query",
        type: "post",
        data: requestJson,
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            var i;
            var result_length = data.length;
            result_size.text("Results: " + result_length);
            for (i = 0; i < result_length; i++) {
                search_results.append("<li>" + data[i]['primary_title'] + "</li>");
            }
        }
    });

}
