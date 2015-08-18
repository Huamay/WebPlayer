/*!
 * WebPlayer v0.1.0 (http://carboncook.github.io/WebPlayer)
 * Copyright 2015- CarbonCook
 * Licensed under the MIT license
 */

//Set up the jwplayer
jwplayer.key = "FWm+IP88iL6P1fsd9gQ9+EuYvq/x6Z8HnQEotw==";

var playerInst = jwplayer( "playerContainer" );
playerInst.setup({
    playlist: /*listpath + rsslist["Sample"],*/[{
        file: "https://ph2doy.dl.openload.io/dl/l/yEltQ_7GSxs/081515_472.mp4"//https://www.youtube.com/watch?v=EK9VI7sakY8"
    }],
    aspectratio: "16:9",
    width: "100%"
});
playerInst.setVolume( 20 );

//Load the page content
for (key in rsslist)
    $( "ul#rssMenu" ).append( "<li><a href=\"#" + key + "\">" + key + "</a></li>" )
$( "ul#rssMenu li:first" ).addClass( "active" );
$( "ul#rssMenu li:first" ).after( "<li role=\"separator\" class=\"divider\"></li>" );

//Respond to operations on the page
function normURL( str ) {
    //alert( str );
    return str;
}

function addURL( url ) {
    if ( ( url = normURL( url ) ) != null ) {
        var playlist = playerInst.getPlaylist();
        playlist.push( { file: url/*, type: "video/flv"*/ } );
        playerInst.load( playlist );
    }
}

$( document ).ready( function() {
    //Add new media URL
    $( "#playButton" ).click( function() {
        // .attr("value") does not make sense
        addURL( $( "#urlInput" ).val() );
        $( "#urlInput" ).val( "" );
    });
    //Select RSS File
    $( "ul#rssMenu li" ).click( function( event ) {
        $( "ul#rssMenu li" ).removeClass( "active" );
        $( event.target ).parent().addClass( "active" );
        playerInst.load( listpath + rsslist[ $( event.target ).html() ] );
    });
});