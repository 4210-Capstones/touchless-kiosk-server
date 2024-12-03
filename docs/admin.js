/*
document.addEventListener("DOMContentLoaded", () => {
    const requestsContainer = document.getElementById("requests");

    // Fetch requests from the backend
    async function fetchRequests() {
        try {
            const response = await fetch("http://localhost:8000/imgrequestform/imgrequests");
            if (!response.ok) throw new Error("Failed to fetch requests");
    
            const requests = await response.json();
            console.log("Fetched requests:", requests);
    
            // Validate requests array
            if (!Array.isArray(requests)) {
                throw new Error("Invalid response: Expected an array");
            }
    
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
    
            if (requestElement) { // Only append valid elements
                requestsContainer.appendChild(requestElement);
            } else {
                console.warn("Skipped invalid request:", request);
            }
        });
    }

    // Create a single request component
    function createRequestComponent(request) {
        console.log("Processing request:", request); // Log the request object
        if (!request.id) {
            console.error("Missing ID in request:", request);
            return null;
        }
    
        // Create HTML for tags with specific color-coding
        let tagsHtml = request.imgreq_tags && request.imgreq_tags.length > 0
            ? request.imgreq_tags.map(tag => `<span class="tag ${getTagClass(tag.tag_name)}">${tag.tag_name}</span>`).join("")
            : "<span class='no-tags'>No Tags</span>";
    
        let imagesHtml = "";
        console.log('Before imagesHTML');
        if (request.imgreq_links && Array.isArray(request.imgreq_links)) {
            console.log('Inside imagesHTML');
            imagesHtml = request.imgreq_links.map(link => {
                console.log('Image link:', link);
                return `<img src="http://localhost:8000${link}" alt="It no work" onerror="this.src='/uploads/img_requests/fallback.jpg';" class="request-image">`;
            }).join("");
        } else {
            imagesHtml = "<p class='no-image'>No Image Available</p>";
        }
        console.log('After imagesHTML');
    
        const requestDiv = document.createElement("div");
        requestDiv.classList.add("request");
    
        requestDiv.id = `request-${request.id}`;
    
        requestDiv.innerHTML = `
            <h3>Request ID: ${request.id}</h3>
            <h3>${request.imgreq_name || "Unknown Name"}</h3>
            <p><strong>Email:</strong> ${request.imgreq_email || "No Email Provided"}</p>
            <p><strong>Message:</strong> ${request.imgreq_message || "No Message Provided"}</p>
            <p><strong>Start Date:</strong> ${
                request.imgreq_startdate ? new Date(request.imgreq_startdate).toLocaleString() : "No Start Date"
            }</p>
            <p><strong>End Date:</strong> ${
                request.imgreq_enddate ? new Date(request.imgreq_enddate).toLocaleString() : "No End Date"
            }</p>
            <div class="tags">${tagsHtml}</div>
            <div class="images">${imagesHtml}</div>            
            <div class="actions">
                <button class="approve" onclick="handleApprove(event, ${request.id})">Approve</button>
                <button class="reject" onclick="handleReject(event, ${request.id})">Reject</button>
            </div>
        `;
    
        return requestDiv;
    }

    // Attach Approve and Reject handlers to the global window object
    window.handleApprove = async function handleApprove(event, requestId) {
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
            alert(`Error: ${error.message}`);
        } finally {
            enableButton(button, "Approve");
        }
    };

    window.handleReject = async function handleReject(event, requestId) {
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
            alert(`Error: ${error.message}`);
        } finally {
            enableButton(button, "Reject");
        }
    };

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
*/