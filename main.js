/*!
 * WebPlayer v0.1.0 (http://carboncook.github.io/WebPlayer)
 * Copyright 2015- CarbonCook
 * Licensed under the MIT license
 */

//Set up the jwplayer
jwplayer.key = "FWm+IP88iL6P1fsd9gQ9+EuYvq/x6Z8HnQEotw==";

var playerInst = jwplayer( "playerContainer" );
playerInst.setup({
    playlist: listpath + rsslist["Sample"],
    aspectratio: "16:9",
    width: "100%"
});
playerInst.setVolume( 20 );

//Load the navbar content
for (key in rsslist)
    $( "ul#rssMenu" ).append( "<li><a href=\"#" + key + "\">" + key + "</a></li>" )
$( "ul#rssMenu li:first" ).addClass( "active" );
$( "ul#rssMenu li:first" ).after( "<li role=\"separator\" class=\"divider\"></li>" );

function rmOldContents() {
    $( ".panel-group" ).remove();
    $( ".pagination" ).children().filter( ":not([id])" ).remove();
}

function addContentToPanelGroup( item, itemIdx, panelIdx ) {
    var accoId = "accordion" + panelIdx;
    var headingId = "heading" + itemIdx, collaId = "collapse" + itemIdx;
    $( "#" + accoId ).append(
        '<div class="panel panel-default">\
            <div class="panel-heading" data-toggle="tooltip" data-html="true" role="tab" id="' + headingId + '">\
        </div>' );
    $( "#" + headingId ).attr( "data-title", "<img src='" + item.children( "jwplayer\\:image" ).html() + "'>" );
    $( "#" + headingId ).append(
        '<h4 class="panel-title">\
            <a role="button" data-toggle="collapse" data-parent="#' + accoId + '" href="#' + collaId + '" aria-expanded="true" aria-controls="' + collaId + '">'
                + itemIdx + '. ' + item.children( "jwplayer\\:title" ).html() +
            '</a>\
        </h4>');
    $( "#" + headingId ).after(
        '<div id="' + collaId + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="' + headingId + '">\
            <div class="row"></div>\
        </div>');
    item.children( "preview:not(:first)" ).each( function( index ) {
        $( "#" + collaId ).children( '.row' ).append(
            '<div class="col-xs-6 col-md-3">\
                <a href="#Preview ' + index + '" class="thumbnail">\
                    <img src="' + $( this ).html() + '" alt="...">\
                </a>\
            </div>');
    });
}

function displayPage( pageIdx ) {
    var n_pages = $( ".pagination" ).children().size() - 2;
    if ( pageIdx < 1 || pageIdx > n_pages )
        return;
    var targ_page = $( ".pagination" ).children().eq( pageIdx );
    if ( targ_page.is( ".active" ) )
        return;
    var acti_page = $( ".pagination" ).children( ".active" );
    acti_page.removeClass( "active" );
    $( "#accordion" + acti_page.children().html() ).addClass( "invisible" );
    targ_page.addClass( "active" );
    $( "#accordion" + targ_page.children().html() ).removeClass( "invisible" );
}

function initConfig() {
    $( "#pagination" ).removeClass( "invisible" );
    $( ".panel-group:not(:first)" ).addClass( "invisible" );
    $( "#paginPrev" ).next().addClass( "active" );
    $('[data-toggle="tooltip"]').tooltip();
    //Select pagination
    $( ".pagination" ).children().click( function( event ) {
        var acti_page = $( ".pagination" ).children( ".active" );
        var targ_page = $( event.target ).parents( "li" );
        if ( targ_page.is( "#paginPrev" ) )
            displayPage( parseInt( acti_page.children().html() ) - 1 );
        else if ( targ_page.is( "#paginNext" ) )
            displayPage( parseInt( acti_page.children().html() ) + 1 );
        else
            displayPage( parseInt( targ_page.children().html() ) );
    });
    //Select video
    $( ".panel-heading" ).click( function( event ) {
        playerInst.playlistItem( parseInt( $( event.target ).html() ) - 1 );
        playerInst.stop();
    });
}

//Load panel groups
function loadPanelGroup( rssUrl ) {
    $.ajax({
        url: rssUrl,
        dataType: 'xml',
        type: 'GET',
        timeout: 2000,
        error: function( xml ) {
            alert( "XML loading error!" );
        },
        success: function( xml ) {
            rmOldContents();
            var items = $( xml ).find( "item" );
            for ( var i = 0; i < items.size(); ) {
                var idx = i / 20 + 1, accoId = "accordion" + idx;
                $( "#pagination" ).before( '<div class="panel-group" id="' + accoId + '" role="tablist" aria-multiselectable="true"></div>' );
                for ( var j = 0; i < items.size() && j < 20; i ++, j ++ )
                    addContentToPanelGroup( items.eq( i ), i + 1, idx );
                $( "#paginNext" ).before( '<li><a href="#' + idx + '">' + idx + '</a></li>' );
            }
            initConfig();
        }
    });
}

//Respond to operations on the page
function normURL( str ) {
    return str;
}

function addURL( url ) {
    if ( ( url = normURL( url ) ) != null ) {
        var playlist = playerInst.getPlaylist();
        playlist.push( { file: url/*, type: "video/flv"*/ } );
        playerInst.load( playlist );
        alert( url );
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
        var rssUrl = listpath + rsslist[ $( event.target ).html() ];
        playerInst.load( rssUrl );
        loadPanelGroup( rssUrl );
    });
    //Back-to-top button
    $( window ).scroll( function () {
        if ( $( this ).scrollTop() != 0 )
            $( '#toTop' ).fadeIn();
        else
            $( '#toTop' ).fadeOut();
    });
});
