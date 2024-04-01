async function sendMessage() {
    const form = document.getElementById('messageForm');
    const token = form.getAttribute('data-csrf-token');
    const firstName = form.getAttribute('data-user-first-name');
    const messageField = document.getElementById('messageField'); // Stelle sicher, dass die ID korrekt ist
    const messageContainer = document.getElementById('messageContainer'); // Definiere, wo Nachrichten angezeigt werden sollen

    const today = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    const datumAlsString = today.toLocaleDateString('en-US', options);

    // Temporäre Nachricht mit neuer Struktur
    messageContainer.innerHTML += /*html*/`
        <div class="chat-bubble sent-message idle">
            <div class="message-info">
                <span class="message-author">${firstName}</span>
                <span class="message-date">${datumAlsString}</span>
                <div class="statusContainer">
                    <span class="material-symbols-outlined sent">done</span>
                </div>
            </div>
            <div class="message-text">
                ${messageField.value} <span style="font-size: 8px; color: red;">(Message not saved yet)</span>
            </div>
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
        document.querySelector('.idle').remove(); // Achte darauf, das korrekt zu selektieren, möglicherweise musst du dies anpassen.

        // Füge die echte Nachricht hinzu, basierend auf der Struktur deiner Antwort
        messageContainer.innerHTML += /*html*/`
            <div class="chat-bubble sent-message">
                <div class="message-info">
                    <span class="message-author">${firstName}</span>
                    <span class="message-date">${responseJson.fields.created_at}</span>
                    <div class="statusContainer">
                        <span class="material-symbols-outlined sent">done</span>
                        <span class="material-symbols-outlined received">done</span>
                    </div>
                </div>
                <div class="message-text">
                    ${messageField.value}
                </div>
            </div>
        `;

        messageField.value = '';

    } catch (e) {
        console.error('Fehler beim Senden der Nachricht:', e);
    }
}
