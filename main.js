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
        file: "http://im.6820a829.b028f5c.cdn2c.videos2.yjcontentdelivery.com/3/c/3cd78117c735cc97cce6ea873035323e1390254930-480-266-400-h264.flv?rs=300&ri=1200&s=1439620390&e=1439793190&h=08e9ca7e5b241c3660cb1800cefcc7cd"
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
    alert( str );
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