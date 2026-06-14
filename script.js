window.addEventListener("load", () => {

    let selectedProduct = "";
    let selectedOS = "";

    const modal = document.getElementById("modal");
    const downloadBtn = document.getElementById("downloadBtn");
    const closeModal = document.getElementById("closeModal");
    const confirmDownload = document.getElementById("confirmDownload");

    // OPEN MODAL
    downloadBtn.addEventListener("click", (e) => {
        e.preventDefault();
        modal.classList.remove("hidden");
    });

    // CLOSE MODAL
    closeModal.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    // PRODUCT SELECT
    document.querySelectorAll(".store-card").forEach(card => {
        card.addEventListener("click", () => {

            document.querySelectorAll(".store-card")
            .forEach(c => c.classList.remove("selected"));

            card.classList.add("selected");

            selectedProduct = card.dataset.product;

            console.log("Product:", selectedProduct);
        });
    });

    // OS SELECT
    document.querySelectorAll(".card-os").forEach(card => {
        card.addEventListener("click", () => {

            document.querySelectorAll(".card-os")
            .forEach(c => c.classList.remove("selected"));

            card.classList.add("selected");

            selectedOS = card.dataset.os;

            console.log("OS:", selectedOS);
        });
    });

    // DOWNLOAD
    confirmDownload.addEventListener("click", () => {

    if (!selectedProduct || !selectedOS) {
        alert("Select product + OS");
        return;
    }

    if (selectedProduct === "arty r" && !isPremium) {
        alert("Premium required");
        return;
    }

    fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user: currentUser || "guest",
            product: selectedProduct,
            os: selectedOS
        })
    });

    const file = `${selectedProduct}-${selectedOS}.zip`;

    const a = document.createElement("a");
    a.href = `downloads/${file}`;
    a.download = file;
    a.click();

    modal.classList.add("hidden");
});

});

function login() {
    const username = prompt("Username:");
    const password = prompt("Password:");

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            alert("Login success: " + data.role);
            localStorage.setItem("role", data.role);
        } else {
            alert("Login failed");
        }
    });
}

function loadLogs() {
    fetch("http://127.0.0.1:5000/logs")
    .then(r => r.json())
    .then(data => {
        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);
    });
}

let currentUser = "guest";

function login() {
    const username = prompt("Username:");

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username})
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === "ok") {
            currentUser = data.user;
            alert("Logged in as " + currentUser);
        }
    });
}