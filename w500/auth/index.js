'use strict';

var ensureAuthenticated = function (req, res, next) {
  if (req.isAuthenticated()) { return next(); }
  res.redirect('/');
};

exports.ensureAuthenticated = ensureAuthenticated;