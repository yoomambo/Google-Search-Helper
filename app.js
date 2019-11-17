const _http = require('http');
const _url = require('url');
const _fs = require('fs');
const _ejs = require('ejs');
const _express = require('express');
let { PythonShell } = require("python-shell");
const port = 8080;

var start = false;
var keyword;

var app = _express();
app.set('port', port);
var server = _http.createServer(function(req, res){
    var url = _url.parse(req.url, true);
    var target;

    if(url.pathname == '/')
        target = __dirname + '/assets/index.html'
    else if(url.pathname == '/search')
        target = __dirname + '/assets/search.html';
    else
        target = 'assets' + url.pathname;

    if(url.query.keyword) {
        keyword = url.query.keyword;
        start = true;
    }
    _fs.readFile(target, function(err, data){
        if(!err){
            var dotoffset = target.lastIndexOf('.');
            var mimetype = dotoffset == -1 ? 'text/plain'
                            : {'.html' : 'text/html',
                                '.ico' : 'image/x-icon',
                                '.jpg' : 'image/jpeg',
                                '.png' : 'image/png',
                                '.gif' : 'image/gif',
                                '.svg' : 'image/svg',
                                '.css' : 'text/css',
                                 '.js' : 'text/javascript',
                            }[ target.substr(dotoffset) ];
            console.log(logtime() + ' >> ' + target + ', ' + mimetype);
            if(mimetype == 'text/html' && start){
                var options = {
                    mode: 'json',
                    pythonOptions: ['-u'],
                    args: [keyword]
                }
            
                PythonShell.run("test.py", options, function(err, res) {
                    if (err) throw err;
                    var results = res[0];
                    console.log(results);
            
                    for(var ele in results)
                        add_result(ele['title'], ele['url'], ele['detail']);
                });
                start = false;
            }
            res.setHeader('Content-type', mimetype);
            res.end(data);
        } else {
            console.log ('file not found: ' + req.url);
            res.writeHead(404, "Not Found");
            res.end();
        }
    });
}).listen(app.get('port'), function(){
    console.log("Server is running on " + app.get('port'));
});

app.get('/search', (req, res) => { console.log("GET Request arrived : " + req.query.keyword) });

function logtime() {

    var date = new Date();
    var hour = date.getHours();
    hour = (hour < 10 ? "0" : "") + hour;
    var min  = date.getMinutes();
    min = (min < 10 ? "0" : "") + min;
    var sec  = date.getSeconds();
    sec = (sec < 10 ? "0" : "") + sec;
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    month = (month < 10 ? "0" : "") + month;
    var day  = date.getDate();
    day = (day < 10 ? "0" : "") + day;

    return year + ":" + month + ":" + day + ":" + hour + ":" + min + ":" + sec;
}

function add_result(title, url, detail){
    
    // var a = document.createElement("a");
    // a.setAttribute('href', url);
    // var text = document.createTextNode(title);

    // var h2 = document.createElement("h2");
    // h2.appendChild(h2);
    // h2.appendChild(text);

	// var header = document.createElement("header");
    // header.setAttribute('class', "major");

    // var div = document.createElement("div");
	// div.setAttribute('class', "result");

	// header.appendChild(h2);
	// div.appendChild(header);
    // div.appendChild(detail);

    // console.log(document);
    // var main = document.getElementById("main");
    // main.appendChild(h2);
}