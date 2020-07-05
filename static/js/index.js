hideChat();

$('#prime').click(function() {
    toggleFab();
});


//Toggle chat and links
function toggleFab() {
    $('.prime').toggleClass('zmdi-comment-outline');
    $('.prime').toggleClass('zmdi-close');
    $('.prime').toggleClass('is-active');
    $('.prime').toggleClass('is-visible');
    $('#prime').toggleClass('is-float');
    $('.chat').toggleClass('is-visible');
    $('.fab').toggleClass('is-visible');
}

function hideChat(hide) {
    $('#chat_converse').css('display', 'block');
}


$('#fab_send').click(function(e) {
    var data_text = $("textarea[id=chatSend]").val()
    PostFunction(data_text)
});

function LastFunction(data) {
    var text = "#chat_converse"
    ul = $("<ul>");
    ul.append("<li>" + data + "</li>");
    $(text).append(ul);
}

function PostFunction(data_text) {
    $.ajax({
        url: "/chat/",
        data: { "text": data_text },
        method: 'POST',
        dataType: "json",
        cache: false,
        beforeSend: function() {
            LastFunction("<div id=chat_response><span class='chat_msg_item chat_msg_item_user' id='chat_msg_item_user'>" + data_text + "</span></div>")
            $("textarea[id=chatSend]").val(' ')
            $('p[id=response]').val(' ')
        },
        success: function(data) {
            LastFunction("<div id=boot_chat><span class='chat_msg_item chat_msg_item_admin'><div class='chat_avatar'><img src='http://res.cloudinary.com/dqvwa7vpe/image/upload/v1496415051/avatar_ma6vug.jpg' /></div><p id="+ data['response'].length+">" + data['response'] + "</p></span></div>")
            var text = "#"+data['response'].length
            var val = data['options']
            ul = $("<ul>");
            for (var i = 0, l = val.length; i < l; ++i) {
                ul.append("<li>" + val[i] + "</li>");
            }
            $(text).append(ul);
            var audio = document.getElementById('myTune');
            var source = document.getElementById('audioSource');
            source.src = data['file_name'];
            audio.load();
            audio.play();
        },
        complete: function() {
            console.log('completed function')
        }
    });
}

