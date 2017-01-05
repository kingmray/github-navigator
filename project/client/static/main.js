$(document).ready(function() {
    $('input[name="query_string"]').focus();
    /*
    $("form").on("submit", function() {
        var query_string = $('input[name="query_string"]').val();
        console.log(query_string);

        $.ajax({
          type: "POST",
          url: "/repositories",
          data : { 'query_string': query_string },
          success: function(results) {
            if (results.results.length > 0) {
              //$('input').hide();
              //$('#try-again').show();
             
              $('#results').html(results.results)
              // $('input').val('')
            } else {
              $('#results').html('Something went terribly wrong! Please try again.')
            }
          },
          error: function(error) {
            console.log(error)
          }
        });
    });
    */
});
