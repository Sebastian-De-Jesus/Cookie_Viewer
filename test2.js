// Using jsdom in node js, troubleshoot of option 2

var fs = require('fs');
var jsdom = require("jsdom");
var http = require("http");


http.createServer(function (request, response) {
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.end('Hello World\n'); 
}).listen(8081); 
console.log('Server running at http://127.0.0.1:8081/');


const data = fs.readFileSync('./test.json', {encoding:'utf8'});
console.log(data);

jsdom.env({
    html: 'http://127.0.0.1:8081/',
    src: [],
    done: function(errors, window) {
  
      var document = window.document;
      
  
      var writerStream = fs.createWriteStream('test.html');
      writerStream.write(data,'UTF8');
      writerStream.end();
      writerStream.on('finish', function() {    console.log("Write completed."); });
      writerStream.on('error', function(err){   console.log(err.stack); }); 
      console.log("Program Ended");
  
    }
  });


