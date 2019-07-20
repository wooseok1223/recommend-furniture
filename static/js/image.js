function showImage() {
    var modern = new Array();
    var natural = new Array();

    for (i = 1;i < 80 ;i++)
    {
	    modern[i] = "/static/img/modern/bedroom/web/A" +i+ ".png";
	    natural[i] = "/static/img/natural/bedroom/web/A" +i+ ".png";
    }
    var imgNum = Math.round(Math.random()* 78);
	var documentid = new Array('modern_choice','natural_choice');
	var objImg = new Array();
	for (i = 0;i < 2 ;i++)
	{
		objImg[i] = document.getElementById(documentid[i]);
	}
	objImg[0].src = modern[imgNum];
	objImg[1].src = natural[imgNum];
}

function showImage2() {
    var modern = new Array();
    var natural = new Array();

    for (i = 1;i < 80 ;i++)
    {
	    modern[i] = "/static/img/modern/livingroom/web/A" +i+ ".png";
	    natural[i] = "/static/img/natural/livingroom/web/A" +i+ ".png";
    }
    var imgNum = Math.round(Math.random()* 78);
	var documentid = new Array('living_modern_choice','living_natural_choice');
	var objImg = new Array();
	for (i = 0;i < 2 ;i++)
	{
		objImg[i] = document.getElementById(documentid[i]);
	}
	objImg[0].src = modern[imgNum];
	objImg[1].src = natural[imgNum];
}


var count = 0;
 
function changevar(){ 
 
    count = count + 1;
    return document.getElementById("viewCount").textContent=count; 
 
}


function nextpage(){
	node = document.getElementById("viewCount").textContent;
	if (node >= 10)
	{
		var aa = document.getElementById('img_total'); 
		aa.innerHTML = "";
		if(node == 10)
		{	
			var tObj = document.getElementById('img_total');
			var next = document.createElement('DIV');

			next.innerHTML = '<button id="data_tt" value = "선택완료"  onclick="text_test();">선택완료</button>';

			tObj.appendChild(next);
		}
	}
	return node;
}

var finaltt = new Array();
var nextindex = new Array();

function j_test(o){
	var tt = $(o).attr('src');
	finaltt.push(tt);
	return finaltt;
}

function text_test(){
    var aa = document.getElementById('img_total');
	aa.innerHTML = "";

	var tObj = document.getElementById('img_total');
	var next = document.createElement('DIV');

	next.innerHTML = '<form action="/result" method="POST"><input type = "text" id="testt2" name = "src" style = "position: static; margin: 0px; width: 0px; height: 0px; top : 520px"></input><button class = "btn-1" onclick="data_tttttt()">결과보기</button> ';

	tObj.appendChild(next);
}


function data_tttttt(){
	var cnt;
	src = finaltt;
	var ttttt = new Array();
	for (cnt = 0;cnt <= 10 ;cnt++)
	{
		var data = new Object();
		data.src = src[cnt];
		ttttt.push(data);
	}
	var test = JSON.stringify(ttttt);
	document.getElementById("testt2").value = src;
}
//	var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(ttttt));
//    alert(dataStr);
//    var downloadAnchorNode = document.createElement('a');
//    downloadAnchorNode.setAttribute("href", dataStr);
//    downloadAnchorNode.setAttribute("download", 'recommend.json');
//    var tObj = document.getElementById('wrap');
//	var next = document.createElement('DIV');
//	tObj.appendChild(downloadAnchorNode);
//	tObj.appendChild(downloadAnchorNode);
//    downloadAnchorNode.click();
//    downloadAnchorNode.remove();
