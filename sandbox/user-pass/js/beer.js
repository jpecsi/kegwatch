var qrcode = new QRCode("qrcode");

const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const consumer = urlParams.get('user')


fetch("https://api.watchmy.beer/pass/user/"+consumer.replace(/\s/g, '+')).then((response) => {
	return response.json()
 }).then((data) => {
	document.getElementById("oz").textContent=data["oz"];
	document.getElementById("bac").textContent=data["bac"];
	document.getElementById("beer").textContent=data["beer"];
 })

function makeCode() {
	qrcode.makeCode(consumer);
	document.getElementById("name").textContent=consumer;
}



window.onload = makeCode();

