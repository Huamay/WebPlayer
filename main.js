/*!
 * WebPlayer v0.1.0 (http://carboncook.github.io/WebPlayer)
 * Copyright 2015- CarbonCook
 * Licensed under the MIT license
 */

jwplayer.key = "FWm+IP88iL6P1fsd9gQ9+EuYvq/x6Z8HnQEotw==";

var playerInst = jwplayer("playerContainer");
playerInst.setup({
    playlist: [{
        file: "https://ph2dot.dl.openload.io/dl/l/3gdfWQ70_TU/heyzo0921.mp4"
    }, {
        file: "https://pgli32.dl.openload.io/dl/l/rS8anF5EjVE/%E7%9B%9C%E5%A2%93%E8%BF%B7%E5%9F%8E~%E9%AD%94%E5%92%92.avi.mp4"
    }, {
        file: "http://159i.com/video/get.php?url=akH1R509cHM6Ly9yZWRpcmVjdG9yLmdvb2dsZXZpZGVvLmNvbS92aWRlb3BsYXliYWNrP3JlcXVpcmVzc2w9eWVzJmlkPWJlMjU2ZmU5ZjdiMWVjNjUmaXRhZz0xOCZzb3VyY2U9cGljYXNhJmNtbz1zZWN1cmVfdHJhbnNwb3J0JTNEeWVzJmlwPTAuMC4wLjAmaXBiaXRzPTAmZXhwaXJlPTE0Mzk2NTc2MzQmc3BhcmFtcz1yZXF1aXJlc3NsLGlkLGl0YWcsc291cmNlLGlwLGlwYml0cyxleHBpcmUmc2lnbmF0dXJlPUQ5OEIwOUZDQzBBNUZCQkU0MjUyRUUwNEZGNERGQTNFNDA0MTIzN0QuQjM1RUQ1QTRBODVCMTdBRUYyRDRFMEFCNzVCMUIxMzU4QUVEQjRDNSZrZXk9bGgx",
        type: "video/mp4"
    }],
    aspectratio: "16:9",
    width: "100%"
});
playerInst.setVolume(20);

function normURL(str){
    return str;
}

function addURL(url){
    if ((url = normURL(url)) != null) {
        var playlist = playerInst.getPlaylist();
        playlist.push({file: url, type: "video/mp4"});
        playerInst.load(playlist);
    }
}

$(document).ready(function(){
  $("#playButton").click(function(){
    // .attr("value") does not make sense
    addURL($("#urlInput").val());
    $("#urlInput").val("");
  });
});