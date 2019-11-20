'use strict';

const passport = require('passport');
var GoogleStrategy = require( 'passport-google-oauth20' ).Strategy
var cookieParser = require('cookie-parser');
var session = require('express-session');
var sync = require('synchronize');
var config = require('./config.json');
let { PythonShell } = require('python-shell');

passport.serializeUser(function(user, done) {
    done(null, user);
});

passport.deserializeUser(function(obj, done) {
    done(null, obj);
});

passport.use(new GoogleStrategy({
    clientID: config['web']['client_id'],
    clientSecret: config['web']['client_secret'],
    callbackURL: config['web']['redirect_uris'][0]
  }, 
  function(accessToken, refreshToken, profile, cb) {
    // asynchronous verification, for effect...
    process.nextTick(function () {
      var nickname = profile.displayName;
      var dir = __dirname + '/../public/uploads/' + nickname;
      var options = {
          mode: 'json',
          pythonOptions: ['-u'],
          args: [dir]
      }
      sync.fiber(function(){
        var results = sync.await(PythonShell.run("./public/python/getUser.py", options, sync.defer()));
      });
    });
    return cb(null, profile);
}));

var setup = function(app){
  app.use(cookieParser());
  app.use(session({
    secret: 'gaejuk2 coding',
    cookie: { maxAge: 60 * 60 * 1000 },
    resave: false,
    saveUninitialized: true
  }));
  app.use(passport.initialize());
  app.use(passport.session());
  
  app.get('/auth/google', passport.authenticate('google', { 
    scope: [ 'profile' ]
  }));
  app.get('/auth/google/callback', passport.authenticate( 'google', { 
    failureRedirect: '/auth/google',
    successRedirect: '/#start'
  }));      
}

exports.setup = setup;
