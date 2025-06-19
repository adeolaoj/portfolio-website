function toggleChat() {
    const widget = document.getElementById('chat-widget');
    widget.style.display = widget.style.display === 'none' ? 'block' : 'none';
}

async function sendMessage() {
    const inputElement = document.getElementById('userInput');
    const input = inputElement.value.trim();
    if (!input) return;

    const msgBox = document.getElementById('messages');
    msgBox.innerHTML += `<div class="user-msg">${input}</div>`;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
        });
        const data = await response.json();
        const botMsg = `bot-msg-${Date.now()}`;
        msgBox.innerHTML += `<div class="bot-msg"><span id="${botMsg}"></span></div>`;

         new Typed(`#${botMsg}`, {
            strings: [data.response],
            typeSpeed: 20,
            showCursor: false,
        });

    } catch (err) {
        msgBox.innerHTML += '<div class="bot-msg"><strong>Bot:</strong> Sorry, looks like something went wrong. But you can always access an offline version of this chatbot at github.com/adeolaoj/portfolio-chatbot</div>';
        console.error(err);
    }

    inputElement.value = "";
    msgBox.scrollTop = msgBox.scrollHeight;
}
