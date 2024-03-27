async function sendMessage() {
    const form = document.getElementById('messageForm');
    const token = form.getAttribute('data-csrf-token');
    const firstName = form.getAttribute('data-user-first-name');
    const messageField = document.getElementById('messageField'); // Stelle sicher, dass die ID korrekt ist
    const messageContainer = document.getElementById('messageContainer'); // Definiere, wo Nachrichten angezeigt werden sollen

    const today = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const datumAlsString = today.toLocaleDateString('en-US', options);

    // Nutze `firstName` statt Django-Variable
    messageContainer.innerHTML += /*html*/`
        <div class="temp-message">
          <span class="color-red">[${datumAlsString}] ${firstName}: <i>${messageField.value}</i></span>
        </div>
        `;

    let fd = new FormData();
    fd.append('textmessage', messageField.value);
    fd.append('csrfmiddlewaretoken', token);

    try {
        let response = await fetch('/chat/', {
            method: 'POST',
            body: fd
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        let jsonResponse = await response.json();
        let responseJson = await JSON.parse(jsonResponse) // Dies bestätigt die Struktur der Antwort.
        // Entferne die temporäre Nachricht
        document.querySelector('.temp-message').remove();

        // Füge die echte Nachricht hinzu, basierend auf der Struktur deiner Antwort
        messageContainer.innerHTML += /*html*/`
            <div>
              <span class="color-gray">[${responseJson.fields.created_at}]</span> ${firstName}: <i>${messageField.value}</i>
            </div>
            `;

        messageField.value = '';

    } catch (e) {
        console.error('Fehler beim Senden der Nachricht:', e);
    }
}
