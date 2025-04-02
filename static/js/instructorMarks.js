const studentsHeader = [
    "First Name",
    "Last Name",
    "Username",
    "Mark",
    "Submission Date",
    "Due Date",
    "Submit Grade"
]

const assignmentsHeader = [
    "Assignment Name",
    "Type",
    "Due Date",
    "Grades"
]

const createDialogForm = (row, value, refetch) => {
    const dialog = document.createElement("dialog");
    const title = document.createElement("h2");
    title.textContent = "Submit grade for " + row["fname"] + " " + row["lname"];
    dialog.appendChild(title);
    const form = document.createElement("form");
    form.classList.add("dialogForm");
    form.method = "dialog";
    const label = document.createElement("label");
    label.textContent = "Enter Grade(%):";
    form.appendChild(label);
    const input = document.createElement("input");
    input.type = "number";
    input.step = "0.01";
    input.value = row["mark"] || "";
    input.placeholder = "80";
    input.name = "grade";
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Submit Grade";
    form.appendChild(input);
    form.appendChild(submitButton);
    dialog.appendChild(form);
    document.body.appendChild(dialog);

    form.addEventListener("submit", async (event) => {
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
        const response = await fetch(`/api${window.location.pathname}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ mark: markValue, student_id: row[value] }),
        });
        if (response.ok) {
            dialog.close();
            refetch("Mark submitted successfully.");
        } else {
            console.error("Error submitting grade:", response.statusText);
        }
    });

    return dialog;
}

const submitGradeCell = (td, row, value, refetch) => {
    td.classList.add("submitGradeCell");
    const button = document.createElement("button");
    button.textContent = "Submit Grade";
    const dialogForm = createDialogForm(row, value, refetch);
    button.addEventListener("click", () => {
        dialogForm.showModal();

    });
    td.appendChild(button);
}

const loadStudentsCell = (td, row, value) => {
    const link = document.createElement("a");
    link.href = window.location.pathname + `/${row[value]}`;
    link.textContent = "View Grades";
    td.appendChild(link);
}

const assignmentsHash = {
    [assignmentsHeader[0]]: "coursework_name",
    [assignmentsHeader[1]]: "coursework_type",
    [assignmentsHeader[2]]: "due_date",
    [assignmentsHeader[3]]: "primary_key"
}

const studentsHash = {
    [studentsHeader[0]]: "fname",
    [studentsHeader[1]]: "lname",
    [studentsHeader[2]]: "username",
    [studentsHeader[3]]: "mark",
    [studentsHeader[4]]: "submission_date",
    [studentsHeader[5]]: "due_date",
    [studentsHeader[6]]: "primary_key"
}


export default {
    assignmentsHeader,
    studentsHeader,
    submitGradeCell,
    loadStudentsCell,
    assignmentsHash,
    studentsHash,
}