let notifier = new AWN()

let app = {

    torrents: function() {
        $('.active-torrents').empty()
        $.get(`/api/qbt/list`, function(data){
            if ( data.torrents.length > 0 ) {
                $('.jumbotron').hide()
            } else {
                $('.jumbotron').show()
            }
            $.each(data.torrents, function(i, v){
                let resumeBtn = "resume-btn";
                let torrentCompleted ;
                if ( v.torrent_completed ) {
                    torrentCompleted = "bg-success" ;
                    resumeBtn = "disabled" ;
                }
                let torrentCard = `<div class="card"><div class="card-body"><h5 class="card-title">${v.torrent_name}</h5><div class="progress"><div class="progress-bar ${torrentCompleted}" role="progressbar progress-bar-striped progress-bar-animated" style="width: ${v.torrent_percentage}%" aria-valuenow="${v.torrent_percentage}" aria-valuemin="0" aria-valuemax="100">${v.torrent_percentage}%</div></div></div><div class="card-footer"></button>&nbsp;<button id="${v.torrent_hash}" class="btn btn-danger delete-btn"><i class="fas fa-trash"></i></button><div class="float-right"><button id="${v.torrent_hash}" class="btn btn-primary resume-btn ${resumeBtn}"><i class="fas fa-play-circle"></i></button>&nbsp;<button id="${v.torrent_hash}" class="btn btn-warning pause-btn"><i class="fas fa-pause-circle"></i></div></div></div><br>` ;
                $('.active-torrents').append(torrentCard) ;
            })
        })
    },

    resume: function( torrentHash ) {
        console.log("resuming torrent: " + torrentHash)
        $.ajax({
            url: '/api/qbt/resume',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(data)
                notifier.success('Download resumed')
            },
            data: JSON.stringify({ "hash": torrentHash })
        });
    },

    pause: function( torrentHash ) {
        console.log("pausing torrent: " + torrentHash)
        $.ajax({
            url: '/api/qbt/pause',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(data)
                notifier.warning('Download paused')
            },
            data: JSON.stringify({ "hash": torrentHash })
        });
    },

    add: function( magnet ) {
        console.log("torrent added")
        $.ajax({
            url: '/api/qbt/add',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(data)
                // refresh torrent list
                app.torrents()
                // close modal
                $("#addTorrentModal").modal('hide');
                notifier.success('Torrent added')
            },
            data: JSON.stringify({ "magnet": magnet })
        });
    },

    delete: function( torrentHash ) {
        console.log("deleting torrent: " + torrentHash)
        $.ajax({
            url: '/api/qbt/delete',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(data)
                notifier.warning('torrent removed')
                app.torrents()
            },
            data: JSON.stringify({ "hash": torrentHash })
        });
    }

}

// perform initial load
app.torrents()
// poll api every 10 seconds
setInterval(function(){ app.torrents() }, 10000)

//  handle resume
$(document).on('click', '.resume-btn', function () {
    app.resume(this.id)
})

// handle pause
$(document).on('click', '.pause-btn', function () {
    app.pause(this.id)
})

// handle delete
$(document).on('click', '.delete-btn', function () {
    app.delete(this.id)
})

// add torrent
$(document).on('click', '.add-torrent-btn', function() {
    if ( $('#mgnt-url').val() != "" ) {
        app.add( $('#mgnt-url').val() )
        return
    }
    notifier.warning('no magnet link')
})


// handle side bar toggle
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});