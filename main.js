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
    }],
    aspectratio: "16:9",
    width: "100%"
});
playerInst.setVolume(20);

function isURL(str){
    return true;
}

function addURL(url){
    if (isURL(url)) {
        var playlist = playerInst.getPlaylist();
        playlist.push({file: url});
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