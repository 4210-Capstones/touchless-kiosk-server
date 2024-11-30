document.addEventListener("DOMContentLoaded", () => {
    const requestsContainer = document.getElementById("requests");

    // Fetch requests from the backend
    async function fetchRequests() {
        try {
            const response = await fetch("http://localhost:8000/imgrequestform/imgrequests");
            if (!response.ok) throw new Error("Failed to fetch requests");
            const requests = await response.json();
            renderRequests(requests);
        } catch (error) {
            console.error("Error fetching requests:", error.message);
        }
    }

    // Render all requests
    function renderRequests(requests) {
        requestsContainer.innerHTML = ""; // Clear the container
        requests.forEach((request) => {
            const requestElement = createRequestComponent(request);
            requestsContainer.appendChild(requestElement);
        });
    }

    // Create a single request component
    function createRequestComponent(request) {
        const requestDiv = document.createElement("div");
        requestDiv.classList.add("request");

        // Add request details
        requestDiv.innerHTML = `
            <h3>${request.imgreq_name}</h3>
            <p><strong>Email:</strong> ${request.imgreq_email}</p>
            <p><strong>Message:</strong> ${request.imgreq_message}</p>
            <p><strong>Start Date:</strong> ${new Date(request.imgreq_startdate).toLocaleString()}</p>
            <p><strong>End Date:</strong> ${new Date(request.imgreq_enddate).toLocaleString()}</p>
            <div class="tags">
                ${request.imgreq_tags ? request.imgreq_tags.map(tag => `<span class="tag">${tag.tag_name}</span>`).join("") : ""}
            </div>
            ${request.imgreq_link ? `<img src="${request.imgreq_link}" alt="Request Image">` : ""}
            <div class="actions">
                <button class="approve" onclick="handleApprove(event, ${request.id})">Approve</button>
                <button class="reject" onclick="handleReject(event, ${request.id})">Reject</button>
            </div>
        `;

        return requestDiv;
    }

    // Handle Approve Action
    async function handleApprove(event, requestId) {
        const button = event.target; // Capture the button clicked
        disableButton(button);
        try {
            const response = await fetch(`http://localhost:8000/imgrequestform/admin/requests/${requestId}/approve`, {
                method: "POST",
            });
            if (!response.ok) throw new Error("Failed to approve request");
            alert("Request approved successfully!");
            fetchRequests(); // Refresh the list
        } catch (error) {
            console.error(error.message);
        } finally {
            enableButton(button, "Approve");
        }
    }

    // Handle Reject Action
    async function handleReject(event, requestId) {
        const button = event.target; // Capture the button clicked
        disableButton(button);
        try {
            const response = await fetch(`http://localhost:8000/imgrequestform/admin/requests/${requestId}/reject`, {
                method: "POST",
            });
            if (!response.ok) throw new Error("Failed to reject request");
            alert("Request rejected successfully!");
            fetchRequests(); // Refresh the list
        } catch (error) {
            console.error(error.message);
        } finally {
            enableButton(button, "Reject");
        }
    }

    // Utility: Disable Button
    function disableButton(button) {
        button.disabled = true;
        button.textContent = "Processing...";
    }

    // Utility: Enable Button
    function enableButton(button, originalText) {
        button.disabled = false;
        button.textContent = originalText;
    }

    // Initial Fetch
    fetchRequests();
});
