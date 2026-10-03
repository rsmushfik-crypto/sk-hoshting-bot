async function getTools() {

    const response =
        await fetch("/api/tools/");

    return await response.json();
}
