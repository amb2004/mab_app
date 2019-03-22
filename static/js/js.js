var i = 0;
$( "div.imgs" )
  .mouseover(function() {
    i += 1;
    $( this ).find( ".button" ).css({ display: "inline" });
  })
  .mouseout(function() {
    $( this ).find( ".button" ).css({ display: "none" });
    
  });

window.onload =function loadDoc() {

	var xhttp = new XMLHttpRequest();

	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		 document.getElementById("section").innerHTML = unescape(JSON.parse(this.responseText).html);
		}
	};

	xhttp.open("GET", "hello", true);
	xhttp.send();
}


function check(element)
{
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    var modal = document.getElementById('myModal');

    modal.style.display = "block";
    
	
	var jsonData = {};
	jsonData["src"]=element.src;

	$.ajax({
	type: 'POST',
	url: 'posts',
	data: JSON.stringify (jsonData),
	success: function(data,stat) {
		
			var aa ="static/img/croped_rect/" 
			aa=aa+ String(data) 
			aa=aa+ ".jpg"
			
			modalImg.src= aa

		},
	contentType: "application/json",
	dataType: 'json'
	});
	
    captionText.innerHTML = element.alt;

    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() { 
      modal.style.display = "none";
    }
}


function del(element)
{
element=element.parentElement
var aa = element.getElementsByTagName("img")[0].getAttribute("src")

var jsonData = {};
jsonData["src"]=aa;

var r = confirm("Are you sure to remove this element?");
if (r == true) {
$.ajax({
    type: 'POST',
    url: 'hello',
    data: JSON.stringify (jsonData),
    success: function(data,stat) {
		

		alert('status: ' + stat);
		location.reload();


		},
    contentType: "application/json",
    dataType: 'json'
});

}}

function edit(element)
{
  console.log(element)
var form=element.parentElement
// console.log(form)
var img=form.parentElement
// console.log(img)
var aa = img.getElementsByTagName("img")[0].getAttribute("src")
console.log(form)
var jj=form.getElementsByTagName("input")[0]
jj.setAttribute("value", aa);


var r = confirm("Are you sure to edit this element?");
if (r == true) {
  form.submit();
}}





 

