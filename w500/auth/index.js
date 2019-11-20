'use strict';

var ensureAuthenticated = function (req, res, next) {
  if (req.isAuthenticated()) { return next(); }
  console.log("Unauthorization");
  res.redirect('/');
};

exports.ensureAuthenticated = ensureAuthenticated;