async function registerUser() {
    loadingBar.classList.remove('hidden');

    const form = document.getElementById('registerForm');
    const token = form.getAttribute('data-csrf-token');
    
    // Prüfe, ob der CSRF-Token vorhanden ist
    if (!token) {
        showError("CSRF-Token fehlt. Bitte laden Sie die Seite neu und versuchen Sie es erneut.");
        return; // Beendet die Funktion frühzeitig, um die Anfrage nicht zu senden
    }

    let fd = new FormData();
    fd.append('csrfmiddlewaretoken', token);
    fd.append('first_name', first_name.value);
    fd.append('last_name', last_name.value);
    fd.append('email', email.value);
    fd.append('username', username.value);
    fd.append('password', password.value);

    try {
        let response = await fetch('/register/', {
            method: 'POST',
            body: fd
        });

        let jsonResponse = await response.json(); // JSON-Objekt nur einmal verarbeiten.

        if (!response.ok) {
            throw new Error(jsonResponse.error); // Fehler werfen, falls vorhanden.
        }
        
        // Erfolg: Logik bleibt gleich.
        resetForm();
        window.location.href = '/login/'; // Weiterleitung nach erfolgreicher Registrierung

    } catch(e) {
        console.log(e);
        showError(e.message);
    } finally {
        // Versichere dich, dass die Loading Bar-Referenz aktuell ist und verstecke sie.
        loadingBar.classList.add('hidden');
    }

    function resetForm() {
        first_name.value = '';
        last_name.value = '';
        email.value = '';
        username.value = '';
        password.value = '';
    }

    function showError(message) {
        // Zeigt die Fehlermeldung an
        document.getElementById('sendBox').innerHTML = `
            <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                Register
            </button>
            <div id="loadingBar" class="mdl-progress mdl-js-progress mdl-progress__indeterminate hidden"></div>
            <span style="color:red;" id="failure">${message}</span>
        `;

        // Re-Initialisiere MDL-Komponenten
        componentHandler.upgradeElements(document.getElementById('sendBox'));
    }
}
