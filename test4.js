// Getting data from json file using file system module, option 2
var fs = require('fs');
const data = fs.readFileSync('./test.json', {encoding:'utf8'});
console.log(data);

// Attempting to insert table data to html file
let temp = document.querySelector("#table-out");
    let out = "";
    for(let cookie of data) {
        

        out += `
            <tr>
                <td>${cookie.name} </td>
                <td>${cookie.usage}</td>
            </tr
        
        `
    }


    temp.innerHTML = out;
    console.log(out);