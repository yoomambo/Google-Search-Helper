var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  if(!req.query.keyword){
    res.render('index.html');
  }
  else{
    res.redirect('/search?keyword=' + req.query.keyword);
  }
});

module.exports = router;
