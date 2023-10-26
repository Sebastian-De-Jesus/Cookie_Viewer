// Get the current tab and list the cookies
browser.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const tab = tabs[0];
    browser.cookies.getAll({ url: tab.url }, function(cookies) {
      const cookieList = document.getElementById("cookie-list");
      cookies.forEach(function(cookie) {
        const li = document.createElement("li");
        li.textContent = `${cookie.name}: ${cookie.value}`;
        cookieList.appendChild(li);
      });
    });
  });
  