async function predictJob() {
    const text = document.getElementById("jobText").value;
    const resultDiv = document.getElementById("result");

    if (!text.trim()) {
        alert("Please enter some text.");
        return;
    }

    resultDiv.style.display = "none";
    resultDiv.className = "result";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        resultDiv.style.display = "block";
        resultDiv.textContent = `Result: ${data.label} (Confidence: ${data.confidence}%)`;

        if (data.label === "Fake") {
            resultDiv.classList.add("fake");
        } else {
            resultDiv.classList.add("real");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to get prediction. Ensure the backend API is running.");
    }
}
