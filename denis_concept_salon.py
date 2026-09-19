// Funcție pentru eliminarea diacriticelor românești
function removeDiacritics(text) {
    if (!text) return "";
    return text
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "") // Elimină diacriticele
        .replace(/ă/g, "a").replace(/Ă/g, "A")
        .replace(/â/g, "a").replace(/Â/g, "A")
        .replace(/î/g, "i").replace(/Î/g, "I")
        .replace(/ș/g, "s").replace(/Ș/g, "S")
        .replace(/ț/g, "t").replace(/Ț/g, "T");
}

// Funcție completă de trimitere mesaj CallMeBot
function sendWhatsAppNotification(phone, rawText, apiKey) {
    const cleanText = removeDiacritics(rawText);
    const encodedText = encodeURIComponent(cleanText);
    const url = `https://api.callmebot.com/whatsapp.php?phone=${phone}&text=${encodedText}&apikey=${apiKey}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                console.log("Mesaj WhatsApp trimis cu succes!");
            } else {
                console.error("Eroare la trimiterea mesajului WhatsApp.");
            }
        })
        .catch(error => {
            console.error("Eroare de rețea:", error);
        });
}

// Exemplu de apel:
// sendWhatsAppNotification("35796005530", "Programarea a fost salvată cu succes!", "9926434");
