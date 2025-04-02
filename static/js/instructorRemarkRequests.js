const remarkHeader = [
    "Student",
    "Coursework",
    "Reason",
    "Status",
    "Approve/Reject"
]

const remarkHash = {
    [remarkHeader[0]]: "student_name",
    [remarkHeader[1]]: "coursework_name",
    [remarkHeader[2]]: "reason",
    [remarkHeader[3]]: "status",
    [remarkHeader[4]]: "primary_key"
}

const createDialogForm = (row, value, refetch) => {
    const dialog = document.createElement("dialog");
    const title = document.createElement("h2");
    title.textContent = "Review remark request for " + row["student_name"] + " on " + row["coursework_name"];
    dialog.appendChild(title);
    const form = document.createElement("form");
    form.classList.add("dialogForm");
    form.method = "dialog";
    const label = document.createElement("label");
    label.textContent = "Enter a New Grade(%):";
    form.appendChild(label);
    const input = document.createElement("input");
    input.type = "number";
    input.step = "0.01";
    input.value = row["mark"] || "";
    input.placeholder = "80";
    input.name = "grade";
    const acceptButton = document.createElement("button");
    acceptButton.type = "submit";
    acceptButton.textContent = "Accept Request";
    acceptButton.classList.add("acceptButton");

    const rejectButton = document.createElement("button");
    rejectButton.type = "submit";
    rejectButton.textContent = "Reject Request";
    rejectButton.classList.add("rejectButton");

    const div = document.createElement("div");
    div.classList.add("buttonContainer");
    div.appendChild(acceptButton);
    div.appendChild(rejectButton);

    form.appendChild(input);
    form.appendChild(div);
    dialog.appendChild(form);
    document.body.appendChild(dialog);
    
    acceptButton.addEventListener("click", async (event) => {
        event.preventDefault();
        const markValue = input.value;
        if (markValue < 0 || markValue > 100) {
            alert("Please enter a valid grade between 0 and 100.");
            return;
        }
        if (!markValue) {
            alert("Please enter a grade.");
            return;
        }
        console.log(markValue, row[value])
        const response = await fetch(`/api${window.location.pathname}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ mark: markValue, remark_request_id: row[value], status: "Approved" }),
        });
        if (response.ok) {
            dialog.close();
            refetch("Remark request accepted successfully.");
        } else {
            console.error("Error accepting remark request:", response.statusText);
        }
    });

    rejectButton.addEventListener("click", async (event) => {
        event.preventDefault();
        const response = await fetch(`/api${window.location.pathname}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ remark_request_id: row[value], status: "Rejected" }),
        });
        if (response.ok) {
            dialog.close();
            refetch("Remark request rejected successfully.");
        } else {
            console.error("Error rejecting remark request:", response.statusText);
        }
    });

    return dialog;
}

const reviewRemarkRequestCell = (td, row, value, refetch) => {
    td.classList.add("remarkRequestCell");

    const button = document.createElement("button");
    button.classList.add("reviewButton");
    button.textContent = "Review Request";
    const dialog = createDialogForm(row, value, refetch);
    button.addEventListener("click", async () => {
        dialog.showModal();
    });
    td.appendChild(button);
}

export default {
    remarkHeader,
    remarkHash,
    reviewRemarkRequestCell
}