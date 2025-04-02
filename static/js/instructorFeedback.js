const feedbackHeader = [
    "Teaching Likes",
    "Teaching Recommendations",
    "Lab Likes",
    "Lab Recommendations",
    "Reviewed"
]

const feedbackHash = {
    [feedbackHeader[0]]: "teaching_likes",
    [feedbackHeader[1]]: "teaching_recommendations",
    [feedbackHeader[2]]: "lab_likes",
    [feedbackHeader[3]]: "lab_recommendations",
    [feedbackHeader[4]]: "primary_key"
}

const reviewFeedbackCell = (td, row, value, refetch) => {
    td.classList.add("feedbackCell");

    const span = document.createElement("span");
    span.textContent = "Not Reviewed";
    span.classList.add("feedbackText");
    const button = document.createElement("button");
    button.classList.add("feedbackButton");
    button.textContent = "Confirm Review";
    button.addEventListener("click", async () => {
        const response = await fetch(`/api${window.location.pathname}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ feedback_id: row[value], reviewed: true }),
        })
        if (response.ok) {
            refetch("Feedback reviewed successfully.");
        } else {
            console.error("Error submitting review:", response.statusText);
        }
    });
    td.appendChild(button);
    td.appendChild(span);    
}

export default {
    feedbackHeader,
    feedbackHash,
    reviewFeedbackCell
}