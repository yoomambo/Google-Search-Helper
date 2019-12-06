var express = require('express');
var multer = require('multer')
var sync = require('synchronize');
var auth = require('../auth/index');
var router = express.Router();
let { PythonShell } = require('python-shell');

const storage = multer.diskStorage({ 
  destination(req, file, callback) {
    var user = req.session.passport.user.id;
    callback(null, __dirname + '/../../crawling_history/database/' + user);
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
  console.log(req.session.passport);
  if(req.session.passport)
    res.render('index', { auth: true, error: false });
  else
    res.render('index', { auth: false, error: false });
});

router.post('/', auth.ensureAuthenticated, upload.array('FILE_TAG', 1), function(req, res, next) {
  var filename = req.files[0].filename;
  if(filename == 'History'){
    var options = {
      mode: 'json',
      pythonOptions: ['-u']
    }

    sync.fiber(function(){
      sync.await(PythonShell.run( __dirname + "../../../crawling_history/database/history_2_pd_db.py", options, sync.defer()));
    });
    res.redirect('/search');
  }
  else
    res.render('index', { auth: false, error: true });
});

module.exports = router;
