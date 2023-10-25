// Testing to see manifest file working
console.log('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')

// Trying to make javascript run python file, option 3
$.ajax({
    type: "POST",
    url: "~/test.py",
    data: { param: text}
  }).done(function( o ) {
     // do something
  });