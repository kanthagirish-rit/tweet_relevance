

function getTrends(){
	data = {"woeid": $('#woeid').val()};

	console.log("called getTrends");
	 
	$.ajax({
		url: "/tweets/start",
		data: data,
		dataType: "json",
		method: "POST",
		success: function(data){
			var html = "";
			var woeid = data.woeid;
			data = data.data;

			for(var i=0;i<data.length;i++){
			    html += "<div id=\"trend-container\" class=\"trend"+i+"\">";
                //html += "onclick=\"getTweets("+i+")\">";
                html += "<form id=\"trend"+i+"\" action=\"/tweets/tweets\" method=\"POST\">";
                html += "<input type='hidden' name='woeid' id='woeid' value='"+woeid+"'>";
                html += "<input type='hidden' name='trend' value='"+data[i].trend.trend+"'>";
                html += "<ul id= \"menu\">";
                html += "<li id=\"list2\">";
                html += "<button type=\"submit\">" + data[i].trend.trend +"</button></li>";
                html += "<li id=\"list2\">" + data[i].count + " tweets</li>"
                html += "<li id=\"list2\">" + data[i].trend.category + "</li>";
                html += "</ul>";
                html += "</form>";
			    html += "</div>";
            }
			$('#container').html(html);
		}
	})
}
		
function getTweets(val){
    console.log(val);
    trend = $('.trend'+val+' input:hidden').val();
    console.log(trend);
    data = {
        "trend": trend,
        "woeid": $('#woeid').val()
    }

    $.ajax({
		url: "/tweets/tweets",
		data: data,
		dataType: "json",
		method: "POST",
		success: function(data){
	        console.log(data);
	    }
	})
}