$(document).ready(function() {
    let courseworkId;
    $(".remark-button").click(function() {
        courseworkId = $(this).data("coursework-id");
        $("#coursework_id").val(courseworkId);
        console.log($(this).serialize());
        $("#remarkModal").fadeIn(200);
    });

    $(".close").click(function() {
        $("#remarkModal").fadeOut(200);
    });

    $("#remarkForm").on("submit", function(e){
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/request-remark",
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('.remark-button[data-coursework-id="' + courseworkId+'"]').replaceWith('<span class="remark-status">Status: Pending</span>')

                    $("#remarkForm")[0].reset();
                    $("#remarkModal").fadeOut(200);
                    $("#message").text(response.message).css("background-color", "#4caf50").removeClass("hidden");
                    
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);

                } else {
                    $("#message").text(response.message).css("background-color", "#ca2525").removeClass("hidden");
                    
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);
                }
            },
            error: function() {
                $("#message").text("An error occurred. Please try again.").css("background-color", "#ca2525").removeClass("hidden");
                    
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);
            }
        });
    });
});