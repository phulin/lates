$(document).ready(function() {
    $(".late-cancel-link").click(function(e) {
        e.preventDefault();

        var li = $(this).parentsUntil("#late-list").last();
        var id = li[0].id.replace("late-", "");
        $.ajax({
            url: id,
            type: "DELETE"
        }).done(function() {
            li.slideUp();
        });
    })
})
