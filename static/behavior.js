$(document).ready(function() {
    $(".late-cancel-link").click(linkClick);

    $("#request-submit").click(function(e) {
        e.preventDefault();

        var haveLates = ($("#no-lates").css("display") == "none");
        $.post("request",
            $("#request").serialize(),
            function(data, textStatus, jqXHR) {
                if (!haveLates) {
                    $("#late-list").show();
                    $("#no-lates").hide();
                }
                var li = constructLate(JSON.parse(data));
                li.hide().appendTo("#late-list").slideDown();
            });
    });
})

var liString = [
'    <li class="late-item" id=""> ',
'        <span class="late-name">{{ late.name }}</span> ',
'        <div class="late-properties"> ',
'            <span class="late-refrigerated"> ',
'            </span> ',
'            <span class="late-cancel"> ',
'                <a href="" class="late-cancel-link">Cancel</a> ',
'            </span> ',
'        </div> ',
'        <div class="clear"></div> ',
'    </li>'].join('\n');

linkClick = function(e) {
    e.preventDefault();

    var li = $(this).parentsUntil("#late-list").last();
    var id = li.attr("id").replace("late-", "");
    $.ajax({
        url: id,
        type: "DELETE"
    }).done(function() {
        li.slideUp(function() {
            li.remove();
            var haveLates = $("#late-list").children().size() > 0;
            if(!haveLates) {
                $("#late-list").slideUp(function() {
                    $("#no-lates").show();
                });
            }
        });
    });
};

function constructLate(late) {
    var li = $(liString);

    li.attr("id", "late-" + late.id);
    li.find(".late-name").text(late.name);
    var refrigerated = late.refrigerated ? "Refrigerated" : "Unrefrigerated";
    li.find(".late-refrigerated").text(refrigerated);
    li.find(".late-cancel-link").attr("href", late.id);
    li.find(".late-cancel-link").click(linkClick);

    return li;
}
