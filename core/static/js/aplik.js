import { das_boot, webpay, afterkey } from "./nicht.js";

fetch("https://quotes15.p.rapidapi.com/quotes/random/?language_code=es",{
    "method": 'GET',
	"headers": {
        'x-rapidapi-host': 'quotes15.p.rapidapi.com',
		'x-rapidapi-key': das_boot
	}
})
.then(response => response.json())
.then(response => {
    console.log(response);
    console.log(response.content);
    document.getElementById('quote').innerHTML = response.content;
    document.getElementById('author').innerHTML = '- ' + response.originator.name + ' -';
})
.catch(err => {
    console.log(err);
})

