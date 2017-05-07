

function getTrends(){
	data = {
	    "woeid": $('#woeid').val(),
	    "category": $('#category').val()
	};

    $('#tweetsContainer').hide();

	$.ajax({
		url: "/tweets/start",
		data: data,
		dataType: "json",
		method: "POST",
		success: function(data){
			var html = "";
			var woeid = data.woeid;
			data = data.data;
            html += "<input type='hidden' name='woeid' id='woeid' value='"+woeid+"'>";
            html += "<div class='trend-container'><span class='trendsTitle'>";
            html += "Trends</span></div>";
            if (data.length > 0){
                for(var i=0;i<data.length;i++){
                    html += "<div class=\"trend-container\" id=\"trend"+i+"\">";

                    html += "<input type='hidden' name='trend' value='"+data[i].trend.trend+"'>";
                    html += "<ul id= \"menu\">";
                    html += "<li id=\"list2\">";
                    html += "<button onclick=\"getTweets('trend"+i+"')\">";
                    html += "<span class=\"trendName\">" + data[i].trend.trend + "</span>";
                    html += "</button></li>";
                    html += "<li id=\"list2\" style=\"line-height: 0.5;\">";
                    html += "<span class=\"trendCount\">" + data[i].count;
                    if (data[i].count == 1){
                        html += " Tweet";
                    } else{
                        html += " Tweets";
                    }
                    html += "</span></li>";
                    html += "</ul>";
                    html += "</div>";
                }
			}
			else {
			    html += "<div class='trend-container'><span class='trendsTitle'>";
                html += "No trends to show</span></div>";
			}
			$('#trendsContainer').html(html);
			$('#trendsContainer').show();
		}
	});
}
		
function getTweets(id){
    trend = $("#"+id+" input:hidden").val();
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
	        var html = "";
	        if (data.tweets.length > 0){
                for (var i=0; i<data.tweets.length; i++){
                    html += "<div class=\"tweet-container\">";
                    html += "<img src=\"" + data.tweets[i].user.profile_background_image_url;
                    html += "\" class=\"avatar\"/>";
                    html += "<div class=\"namegroup\"><span class=\"fullname\"><strong>";
                    html += data.tweets[i].user.name + "</strong></span>";
                    html += "<span class=\"username\">@";
                    html += data.tweets[i].user.screen_name + "</span>";
                    html += "</div>";
                    html += "<div class=\"textgroup\"><p class=\"tweetText\">";
                    html += data.tweets[i].text;
                    html += "</p></div>";
                    html += "<div class=\"detailsgroup\"><span class=\"details\">Favorites:"
                    html += data.tweets[i].favorite_count + "</span>";
                    html += "<span class=\"details\">Retweets:" + data.tweets[i].retweet_count;
                    html += "</span>";
                    html += "<span class=\"tweetlink\"><a href=\"https://twitter.com/";
                    html += data.tweets[i].user.screen_name + "/status/";
                    html += data.tweets[i].id_str + "\">Tweet link<a/>";
                    html += "</span>";
                    html += "</div>"
                    html += "</div>";
                    console.log(html);
                }
            } else {
                html += "<div class=\"tweet-container\"><div class=\"textgroup\">";
                html += "<p class=\"tweetText\">Oops! No tweets to show</p></div>";
            }
	        $('#tweetsContainer').html(html);
	        $('#tweetsContainer').show();
	    }
	});
}