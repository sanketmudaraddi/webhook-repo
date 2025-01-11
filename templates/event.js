async function fetchEvents() {
    const response = await fetch('http://localhost:5000/events');
    const events = await response.json();

    const eventsContainer = document.getElementById('events');
    eventsContainer.innerHTML = '';

    events.forEach(event => {
        const eventElement = document.createElement('p');
        let displayMessage = `${event.author} `;
        
        if (event.action === "push") {
            displayMessage += `pushed to ${event.to_branch} on ${new Date(event.timestamp).toLocaleString()}`;
        } else if (event.action === "pull_request") {
            displayMessage += `submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toLocaleString()}`;
        } else if (event.action === "merge") {
            displayMessage += `merged branch ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toLocaleString()}`;
        }

        eventElement.textContent = displayMessage;
        eventsContainer.appendChild(eventElement);
    });
}

setInterval(fetchEvents, 15000);  // Poll every 15 seconds
fetchEvents();  // Initial fetch on load
