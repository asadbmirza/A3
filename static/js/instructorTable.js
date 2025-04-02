import instructorMarks from "./instructorMarks.js";
import instructorFeedback from "./instructorFeedback.js";
import instructorRemarkRequests from "./instructorRemarkRequests.js";

const { assignmentsHeader, studentsHeader, loadStudentsCell, submitGradeCell, assignmentsHash, studentsHash } = instructorMarks;
const { feedbackHeader, feedbackHash, reviewFeedbackCell } = instructorFeedback;
const { remarkHash, remarkHeader, reviewRemarkRequestCell } = instructorRemarkRequests;

const fetchData = async () => {
    const rawData = await fetch(`/api${window.location.pathname}`);
    const data = await rawData.json();
    renderTable(data);
}

const refetchData = (message) => {
    alert(message)
    fetchData()
}

document.addEventListener("DOMContentLoaded", fetchData);
const tbody = document.querySelector("tbody");
const thead = document.querySelector("thead");
const contentHeader = document.getElementById("contentHeader");

const headerHash = {
    "Coursework": assignmentsHeader,
    "Students": studentsHeader,
    "Feedback": feedbackHeader,
    "RemarkRequest": remarkHeader
}

const bodyHashes = {
    "Coursework": assignmentsHash,
    "Students": studentsHash,
    "Feedback": feedbackHash,
    "RemarkRequest": remarkHash
}


const primaryKeyCellHash = {
    "Coursework": loadStudentsCell,
    "Students": submitGradeCell,
    "Feedback": reviewFeedbackCell,
    "RemarkRequest": reviewRemarkRequestCell
}


const renderTable = (data) => {
    tbody.innerHTML = '';
    thead.innerHTML = '';
    console.log(data)
    contentHeader.textContent = data.header
    renderHeader(headerHash[data.class])
    if (data.results.length === 0) {
        renderEmptyTable(data)
        return
    }
    renderBody(data)
    
}


const renderEmptyTable = (data) => {
    const emptyRow = document.createElement("tr");
    const emptyCell = document.createElement("td");
    emptyCell.classList.add("emptyCell");
    emptyCell.colSpan = headerHash[data.class].length;
    emptyCell.textContent = "No Data Available";
    emptyRow.appendChild(emptyCell);
    tbody.appendChild(emptyRow);
}

const renderHeader = (headers) => {
    const headerRow = document.createElement("tr");
    headers.forEach((header) => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
}


const renderBody = (data) => {
    const headers = headerHash[data.class]
    const content = data.results;
    const hash = bodyHashes[data.class]
    content.forEach((row) => {
        const tr = document.createElement("tr");
        headers.forEach((header) => {
            const td = document.createElement("td");
            const value = row[hash[header]];
            if (hash[header] == "primary_key") {
                td.classList.add("primaryKeyCell")
                primaryKeyCellHash[data.class](td, row, value, refetchData)
            } else {

                if (value === null || value === undefined) {
                    td.textContent = "No " + header;
                    td.classList.add("emptyCell")
                } else {
                    td.textContent = value;
                }
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
};
