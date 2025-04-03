$(document).ready(function() {
    $("#feedbackForm").on("submit", function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/submit-feedback",
            data: $(this).serialize(),
            success: function(response) {
                if(response.success) {
                    $("#feedbackForm")[0].reset();
                    $("#message").text(response.message).css("background-color", "#4caf50").removeClass("hidden");
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);
                } else{
                    $("#message").text(response.message).css("background-color", "#ca2525").removeClass("hidden");
                    
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);
                }
            },
            error: function() {
                $("#message").text(response.message).css("background-color", "#ca2525").removeClass("hidden");
                    
                    setTimeout(function () {
                        $("#message").fadeOut(200, function() {
                            $(this).addClass("hidden").css("background-color", "");
                        });
                    }, 3000);
            }
        });
    });
});