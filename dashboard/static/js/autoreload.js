document.addEventListener('DOMContentLoaded', function() {

    var autoReloadToggle = document.getElementById('autoreload');
    var timeout = null;

    if (getAutoReload()) {
        autoReloadToggle.checked = true;
        scheduleReload();
    } else {
        autoReloadToggle.checked = false;
    }

    function getAutoReload() {
        return (localStorage.getItem("autoReload") === "true");
    }

    function setAutoReload(event) {
        if (autoReloadToggle.checked) {
            localStorage.setItem("autoReload", true);
            scheduleReload();
        } else {
            localStorage.setItem("autoReload", false);
            abortReload();
        }
    }

    autoReloadToggle.addEventListener('change', setAutoReload);

    function scheduleReload() {
        timeout = setTimeout(() => {
            location.reload();
        }, 5000)
    }

    function abortReload() {
        if (timeout !== null) {
            clearTimeout(timeout);
        }
    }

});
