// Using fetch API to gather data, option 1

fetch("test.json")
.then(res => res.json())
.then(cookies => {
    let temp = document.querySelector("#table-out");
    let out = "";
    for(let cookie of cookies) {
        

        out += `
            <tr>
                <td>${cookie.name} </td>
                <td>${cookie.usage}</td>
            </tr
        
        `
    }


    temp.innerHTML = out;
    console.log(out);
});


