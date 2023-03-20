$(document).ready(function() {
    user_name = $('.name');
    user_list = [];
    for (i=0; i<user_name.length; i++) {
        user_list.push(user_name[i].textContent)
    };
    console.log(user_list)
    for(i=0; i<user_list.length; i++){
        $.ajax({
            type: "GET",
            url: 'https://api.github.com/users/' + user_list[i],
            dataType: "json",
            success: function(data){
                $('#' + data.login).html('<a href=' + data.html_url + '><img width=100 heigth=100 style="border-radius: 50%;" src=' + data.avatar_url + ' alt="NO IMAGE"></a>');
            },
            error: function(data)
            {
                alert('Not working');
            }
        });
    };
});
