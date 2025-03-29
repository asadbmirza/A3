const fetchInstructorMarks = async () => {
    const rawData = await fetch("/assigned-coursework");
    const data = await rawData.json();
    console.log(data)
    renderTable(data);
}

document.addEventListener("DOMContentLoaded", fetchInstructorMarks);
const tbody = document.querySelector("tbody");

const renderTable = (data) => {
    tbody.innerHTML = '';

    if (data.length === 0) {
        renderEmptyTable()
        return
    }
    renderBody(data)
    
}


const renderEmptyTable = () => {
    const emptyRow = document.createElement("tr");
    const emptyCell = document.createElement("td");
    emptyCell.classList.add("emptyCell");
    emptyCell.colSpan = 3;
    emptyCell.textContent = "No Marks Available";
    emptyRow.appendChild(emptyCell);
    tbody.appendChild(emptyRow);
}


const renderBody = (content) => {
    content.forEach((index) => {
        const row = document.createElement("tr")
        Object.values(index).forEach(value => {
            const td = document.createElement("td");
            if (typeof value == "string") {
              td.textContent = value;
              row.appendChild(td);
            }
            else if (Array.isArray(value)) {
                const link = document.createElement("a");
                link.textContent = "View Grades";
                link.href = `${index.coursework_id}/grades`
                td.appendChild(link)
                row.appendChild(td);
            }
        });
        tbody.appendChild(row);
    })

};
