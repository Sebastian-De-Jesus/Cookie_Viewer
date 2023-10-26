function start()
{

const fs = require('fs');
const glob = require('glob');
const sqlite3 = require('sqlite3').verbose();
const os = require('os');
const jsonfile = require('jsonfile');
const { join } = require('path');

function clearFile(fileName = 'result.txt') {
    // Checks if the file exists and deletes its contents if it does.
    if (fs.existsSync(fileName)) {
        fs.writeFileSync(fileName, '');
    }
}

// Finding the user's correct USER name that will be needed to find the user's file path for cookies.
const user = os.userInfo().username;

// Using pattern recognition to find the correct cookie path for users, and saving the value to a variable called profileFolder.
const pattern = `/Users/${user}/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite`;
const matchingPaths = glob.sync(pattern);
const profileFolder = matchingPaths[0];

// Printing out the user's folder path for the cookies folder for Firefox.
console.log(`${profileFolder}\n`);

// Connect to the SQLite database.
const db = new sqlite3.Database(profileFolder);

// Cookie Request
db.serialize(() => {
    db.each("SELECT name, value, host, path, expiry FROM moz_cookies", (err, row) => {
        if (err) {
            console.error(err.message);
        } else {
            const { name, value, host, path, expiry } = row;
            
            // Loop through all cookies and verify which ones are found within the cookie database.
            // Save the found cookies to an array called container.
            const container = [];
            cookiesFiles = jsonfile.readFileSync('cookie-database.json');
            const x = cookiesFiles.map(cookie => cookie.name);
            const y = cookiesFiles.map(cookie => cookie.purpose);

            x.forEach((search, i) => {
                if (name === search) {
                    const result = {
                        NAME: name,
                        PURPOSE: y[i]
                    };
                    container.push(result);
                }
            });

            // Create a JSON file for JavaScript (1st option).
            const jsonFileName = 'result.json';
            jsonfile.writeFileSync(jsonFileName, container, { spaces: 4 });

            // Create an HTML table that can be used directly in an extension popup (2nd option).
            const df = container;
            const htmlTable = `<table>${df.map(row => `<tr><td>${row.NAME}</td><td>${row.PURPOSE}</td></tr>`).join('')}</table>`;
            fs.writeFileSync('result.html', htmlTable);
        }
    });
});

db.close();

} start();


function start2() {
    // Getting data from json file using file system module, option 2
var fs = require('fs');
const data = fs.readFileSync('./result.json', {encoding:'utf8'});
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
} start2();

