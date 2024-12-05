$(function () {
    $("#play-query-text").autocomplete({
        minLength: 2,
        source: function (request, response) {
            $.ajax({
                url: "/populate",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function (data) {
                    response(data.results);
                },
                error: function (xhr, status, error) {
                    alert("Something went wrong. Please try again later.");
                }
            });
        },
        select: function (event, ui) {
            $("#selected-playlist").val(ui.item.value);
            $("#play-query-text").val(ui.item.label.toString());
            return false;
        },
        focus: function (event, ui) {
            $("#selected-playlist").val(ui.item.value);
            $("#play-query-text").val(ui.item.label.toString());
            return false;
        },
    });

    // Execute a function when the user releases a key on the keyboard
    $("#play-query-text").on("keyup", function (event) {
        onEnterPress(event, function () {
            onSearchBtnClick();
        });
    });
});

async function onSearchBtnClick() {
    let playId = $("#selected-playlist").val();

    if (!playId || playId.trim().length === 0) {
        return false;
    }

    await doSearch(playId, false);
}

$("#play-search").click(async function (e) {
    await onSearchBtnClick();
});

$("#random-play-search").click(async function (e) {
    await doSearch("", true);
});

async function doSearch(playId, isRandom = false) {
    const baseEndpoint = isRandom ? "search-random" : "search";
    let endpoint = baseEndpoint;
    if (!isRandom) {
        endpoint = `${baseEndpoint}?q=${playId}`;
    }
    else {
        const uuid = generateUUID();
        endpoint = `${baseEndpoint}?uuid=${uuid}`;
    }
    try {
        waitScreen();
        let result = await doAjax(`/${endpoint}`, "GET");
        allClearScreen();
        onSuccess(result);
    } catch (error) {
        alert("Something went wrong. Please try again later.");
        allClearScreen();
    }
}

function onSuccess(result) {
    clearScreenForResults();
    prepScreenForResults();
    clearAllInputs();

    let results = result.results;
    for (let index = 0; index < result.count; index++) {
        const listItem = $('<li>').addClass('item-thumbs span4 design').attr('data-id', `id-${index}`).attr('data-type', 'web');
        const outerDiv = $('<div>').addClass('item');
        if (index === 0) outerDiv.addClass('query-item');
        const h5 = $('<h5>').text('Query');
        const figure = $('<figure>');
        const div = $('<div>');
        const img = $('<img>').attr('id', `img-id-${index}`).attr('alt', '');
        if (results[index][1] === "None") {
            img.attr("src", "/img/spotify.png");
        } else {
            img.attr("src", results[index][2]);
        }
        img.width('90%');
        img.css("margin", "auto");
        img.css("border", "solid 0.1em black");
        img.error(function () {
            this.src = "/img/spotify.png";
        });
        const h6 = $('<h6>').attr('id', `name-id-${index}`).text(results[index][1]);
        const a = $('<a>').attr('href', `https://open.spotify.com/playlist/${results[index][0]}`)
            .attr('id', `link-id-${index}`)
            .attr('target', '_blank')
            .text(`Link::${results[index][0]}`);

        div.append(img, h6, a);
        figure.append(div);
        outerDiv.append(h5, figure);
        listItem.append(outerDiv);
        $('#thumbs').append(listItem);
    }

    $('#projects').css('visibility', 'visible');
}
