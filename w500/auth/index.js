'use strict';

var ensureAuthenticated = function (req, res, next) {
  if (req.isAuthenticated()) { return next(); }
  res.redirect('/auth/google');
};

exports.ensureAuthenticated = ensureAuthenticated;