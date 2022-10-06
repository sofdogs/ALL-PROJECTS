var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var PORT = process.env.PORT || 3000;


var fs = require('fs');


var tweetinfo = []

//load the input file
fs.readFile('favs.json', 'utf8', function readFileCallback(err,data ){
  if(err){
    req.log.info('cannot load a file:' + fileFolder + '/' + _file_name)
    throw err;
  }
  else{
    let tweetData = JSON.parse(data)
    tweetData.forEach(function(element) {
      tweetinfo.push({time:element.created_at,tweetid:element.id,tweettext:element.text,
        id:element.user.id,name:element.user.name,screen:element.user.screen_name});
    });
  }
});
 
var searchinfo = [];

//Date for new tweets
var today = new Date();
today = Date(Date.now());

app.use(express.static(__dirname));
app.use(bodyParser.json());

//Get functions
//Shows user info
app.get('/tweets', function(req, res) {
  res.send({ tweets: tweetinfo});
});

//Shows tweet info
app.get('/tweetinfo', function(req, res) {
  res.send({ tweetinfo: tweetinfo});
});

//Shows searched tweets
app.get('/searchinfo', function(req, res){
  res.send({ searchinfo: searchinfo})
});

//Post functions
//Posts created tweets
app.post('/tweetinfo', function(req, res) {
  const tweetId3 = req.body.tweetid;
  
  const words = tweetId3.split(';');

  var ID = 
  tweetinfo.push({
    tweetid: words[0],
    tweettext: words[1],
    time: today

  });

  res.send('Successfully created tweet!');

});

//Posts searched tweets
app.post('/searchinfo', function(req, res) {
  var searchedid = req.body.tID;
  var temptext = "";
  var temptime = "";

  console.log(searchedid)
  tweetinfo.forEach(function(tweet, index) {
    if (tweet.tweetid == searchedid) {
      temptime = tweet.tweettext;
      temptext = tweet.time;

      searchinfo.push({
        tID: searchedid,
        tweettext2: temptext,
        tweettime: temptime
      });
    }
  })


  res.send('Shown tweet');
});

//Update
app.put('/tweets/:nm', function(req, res) {
  var nm = req.params.nm;
  var newName = req.body.sc;
  var found = false

  tweetinfo.forEach(function(tweet, index){
    if (!found && tweet.name == nm) {
      tweet.screen = newName;
    }

  });

  res.send('Successfully updated tweet');

});

//Delete 
app.delete('/tweetinfo/:tweetid', function(req, res) {
  var id = req.body.tweetid;   
  console.log(id);
  var found = false;

  tweetinfo.forEach(function(tweet, index){
    if (!found && tweet.tweetid == Number(id)) {
      tweetinfo.splice(index, 1);
    }

  });
  res.send('Successfully deleted product');

});


app.listen(PORT, function() {
  console.log('Server listening on ' + PORT);
});