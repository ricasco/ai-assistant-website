document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded");
    // Check if DOMPurify is loaded
    console.log(DOMPurify);

    const form = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    // Close chat functionality
    const closeChatButton = document.getElementById('close-chat');
    closeChatButton.addEventListener('click', function() {
        window.parent.postMessage('closeChat', '*');
    });

    function displayMessage(message, className) {
        console.log("Displaying message");
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);

        // Automatically convert URLs to clickable links
        const urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        let linkifiedMessage = message.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
        });

        console.log("Linkified message:", linkifiedMessage);

        // Configuring DOMPurify to allow <a> tags and their attributes
        DOMPurify.setConfig({
            ADD_ATTR: ['target'], // Allow 'target' attribute
            ADD_TAGS: ['a'] // Allow 'a' tags
        });

        let sanitizedMessage = DOMPurify.sanitize(linkifiedMessage, {ADD_ATTR: ['target'], ADD_TAGS: ['a']});
        console.log("Sanitized message:", sanitizedMessage);

        messageDiv.innerHTML = sanitizedMessage;
        chatMessages.appendChild(messageDiv);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleResponse(response) {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(err => {
                const errorMessage = err.error || 'Unknown server error';
                throw new Error(errorMessage);
            })
            .catch(() => {
                throw new Error('Error processing the response');
            });
        }
    }

    function showTypingAnimation() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'dot-typing');

        // Include the bot profile image with the dots
        const profileImgHtml = '<img src="/static/botbuddylogo2.jpeg" class="profile-pic">';
        const dotsHtml = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';

        typingDiv.innerHTML = profileImgHtml + dotsHtml;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }

    function hideTypingAnimation() {
        const typingDiv = document.querySelector('.dot-typing');
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    function sendMessageToChat(userMessage) {
        console.log("Sending message:", userMessage);
        displayMessage(userMessage, 'user-message');
        messageInput.value = '';
        showTypingAnimation(); // Show typing animation

        fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userMessage })
        })
        .then(handleResponse) // Use the existing handleResponse function
        .then(data => {
            hideTypingAnimation(); // Hide typing animation before displaying the new message
            displayMessage(data.message, 'gpt-message');
        })
        .catch((error) => {
            console.error('Request failed:', error);
            hideTypingAnimation(); // Ensure to hide typing animation even on error
            displayMessage('An error occurred. Please try again later.', 'error-message');
        });
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const userMessage = messageInput.value.trim();
        if (userMessage) {
            sendMessageToChat(userMessage);
        }
    });
});
