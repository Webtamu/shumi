function changeText(): void {
    const title = document.getElementById("title");
    if (title) {
        title.innerText = "Hello from TypeScript!";
    }
}