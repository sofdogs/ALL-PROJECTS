
$(function() {
   //Get 
   $('#get-button').on('click', function() {
        $.ajax({
            url: '/tweets',
            contentType: 'application/json',
            success: function(response) {
    
                let tbodyEl = $('#namebody');

                tbodyEl.html('');

                response.tweets.forEach(function(tweet){
                    tbodyEl.append('\
                        <tr>\
                        <td class="id">' + tweet.id + '</td>\
                        <td><input type="text" class="name form-control" value="' + tweet.screen +'"></td>\
                        <td><input type="text" class="name form-control" value="' + tweet.name +'"></td>\
                        <td>\
                        </td>\
                        </tr>\
                        ');
                });
            },
            error: function () {

            }
        });
    });


    //Get tweets
    $('#get-tweets-button').on('click', function(){
        $.ajax({

            url:'/tweetinfo',
            contentType: 'application/json',
            success: function(response) {

                console.log(response)
                let tbodyEl2 = $('#tweetbody');

                tbodyEl2.html('');

                response.tweetinfo.forEach(function(tweetinfo){
                    tbodyEl2.append('\
                        <tr>\
                        <td class="tweetid">' + tweetinfo.tweetid + '</td>\
                        <td><input type="text" class="name form-control" value="' + tweetinfo.tweettext +'"></td>\
                        <td><input type="text" class="name form-control" value="' + tweetinfo.time +'"></td>\
                        <td>\
                        </td>\
                        </tr>\
                        ');
               
            });
            },
            error: function() {

            }
            
        });
    });

    //Get searched tweets
    $('#get-searched-tweets').on('click', function() {
        $.ajax({
            url: '/searchinfo',
            contentType: 'application/json',
            success: function(response) {
    
                let tbodyEl3 = $('#searchbody');

                tbodyEl3.html('');

                response.searchinfo.forEach(function(searchinfo){
                    tbodyEl3.append('\
                        <tr>\
                        <td class="tweetid2">' + searchinfo.tID + '</td>\
                        <td><input type="text" class="name form-control" value="' + searchinfo.tweettime +'"></td>\
                        <td><input type="text" class="name form-control" value="' + searchinfo.tweettext2 +'"></td>\
                        <td>\
                        </td>\
                        </tr>\
                        ');
                });
            },
            error: function () {

            }
        });
    });


  //CREATE
  $('#create-form').on('submit', function(event){
        event.preventDefault();

        var createInput = $('#create-input');

        $.ajax({
            url: '/tweetinfo',
            method: 'POST',

            //If error, possibly look at this later on to change to contentType
            contentType: 'application/json',
            data: JSON.stringify({ tweetid: createInput.val() }),
            success: function(response) {
                console.log(response);
                createInput.val('');
                $('#get-tweets-button').click();

            }
        });
  });

    //Create searched tweets
  $('#search-form').on('submit', function(event){
    event.preventDefault();
    var createInput2 = $('#search-input');
    
    $.ajax({
        url: '/searchinfo',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ tID: createInput2.val() }),
        success: function(response) {
            console.log(response);
            createInput2.val('');
            $('#get-searched-tweets').click();
        }
    });
  });

  //UPDATE/PUT
  $("#update-user").on('submit', function(event){
      event.preventDefault();
    var updateInput = $('#update-input');
    var inpString = updateInput.val();

    const spl = inpString.split(';');

    var nm = spl[0];
    var sc = spl[1];
    
    $.ajax({
        url: '/tweets/' + nm,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ sc: sc }),
        success: function(response){
            console.log(response);
            $('#get-button').click();
        }
    });

  });


  //DELETE
  $("#delete-form").on('submit', function() {
    var id = $('#delete-input')
    event.preventDefault();

    $.ajax({
        url: '/tweetinfo/' + id,
        method: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({ tweetid: id.val()}),
        success: function(response) {
            console.log(response);
            id.val('');
            $('#get-tweets-button').click();
            
        }

    });

  });


});


                    
   