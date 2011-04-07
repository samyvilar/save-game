// The following script is a fallback for the autofocus functionality in
// case the browser does not fully support HTML5.
$(document).ready(function() {
    if (!("autofocus" in document.createElement("input"))) {
        $("#username").focus();
    }
});