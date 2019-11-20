var express = require('express');
var multer = require('multer')
var sync = require('synchronize');
var auth = require('../auth/index');
var router = express.Router();
let { PythonShell } = require('python-shell');

const storage = multer.diskStorage({ 
  destination(req, file, callback) {
    var user = req.session.passport.user.displayName
    callback(null, __dirname + '/../public/uploads/' + user); 
  }, 
  filename(req, file, callback) {
    callback(null, file.originalname); 
  } 
}); 

const upload = multer({ 
  storage
});


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { error: false });
});

router.post('/', auth.ensureAuthenticated, upload.array('FILE_TAG', 1), function(req, res, next) {
  var filename = req.files[0].filename;
  if(filename == 'test.py'){
    var options = {
      mode: 'json',
      pythonOptions: ['-u'],
      args: [req.session.passport.user.displayName]
    }

    sync.fiber(function(){
      var results = sync.await(PythonShell.run("./public/python/test.py", options, sync.defer()));
    });
    res.redirect('/search');
  }
  else
    res.render('index', { error: true });
});

module.exports = router;
