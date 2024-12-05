function onEnterPress(event, callback) {
    // Number 13 is the "Enter" key on the keyboard
    var code;
    if (event.key !== undefined) {
        code = event.key;
    } else if (event.keyIdentifier !== undefined) {
        code = event.keyIdentifier;
    } else if (event.keyCode !== undefined) {
        code = event.keyCode;
    }

    if (code === 'Enter' || code === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        callback()
    }
}

async function doAjax(url, actionType, ajaxArgs) {
    let result = await $.ajax({
        url: url,
        type: actionType,
        data: ajaxArgs
    });
    return result;
}

function isArray(value) {
    return value && typeof value === 'object' && value.constructor === Array;
}

function isObject(value) {
    return value && typeof value === 'object' && value.constructor === Object;
}

function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
    );
}

function generateUUID() {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
        return crypto.randomUUID();
    } else {
        return uuidv4();
    }
}
