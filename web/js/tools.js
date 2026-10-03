let allTools = [];

async function loadTools() {

    allTools = await getTools();

    renderTools(allTools);
}


function renderTools(tools) {

    const container =
        document.getElementById("tools");

    container.innerHTML = "";

    tools.forEach(tool => {

        const card =
            document.createElement("div");

        card.className = "card";

        card.innerHTML = `
            <small>
                ${tool.category}
            </small>

            <h3>
                ${tool.name}
            </h3>
        `;

        card.onclick = () => {

            window.location.href =
                `/tool.html?tool=${tool.slug}`;
        };

        container.appendChild(card);

    });
}


document
    .getElementById("search")
    .addEventListener(
        "input",
        function () {

            const query =
                this.value.toLowerCase();

            const filtered =
                allTools.filter(tool =>
                    tool.name
                        .toLowerCase()
                        .includes(query)
                );

            renderTools(filtered);
        }
    );


loadTools();
