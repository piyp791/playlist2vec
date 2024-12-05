function waitScreen() {
    $('#projects').css('visibility', 'hidden');
    $('#thumbs').html('');
    $("#loader").show();
    $("#legend").hide();
    reAlignSearchBars('no-result');

    $("#play-search").attr("disabled", true);
    $("#random-play-search").attr("disabled", true);
}

function clearScreenForResults() {
    $('#projects').css('visibility', 'hidden');
    $('#thumbs').html('');
    $("#loader").hide();

    $("#play-search").attr("disabled", false);
    $("#random-play-search").attr("disabled", false);
}

function prepScreenForResults() {
    $("#legend").show();
    $("#legend").css("text-align", "center");
    reAlignSearchBars("result");
}

function reAlignSearchBars(screenType) {

    if (screenType === "no-result") {

        $("#search-bar-div").removeClass("span4");
        $("#random-div").removeClass("span4");
        $("#legend").hide();

        $("#search-bar-div").addClass("span6");
        $("#random-div").addClass("span6");
    } else if (screenType === "result") {
        $("#search-bar-div").removeClass("span6");
        $("#random-div").removeClass("span6");
        $("#search-bar-div").addClass("span4");
        $("#random-div").addClass("span4");
        $("#legend").attr("display", "block");
    }
}

function allClearScreen() {
    $("#loader").hide();
    $("#legend").hide();
    $('#thumbs').html('');
}

function clearAllInputs(){
    $("#selected-playlist").val("");
    $("#play-query-text").val("");
}