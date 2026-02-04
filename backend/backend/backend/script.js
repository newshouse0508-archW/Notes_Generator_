const button = document.getElementById("generateBtn");
const output = document.getElementById("output");

button.addEventListener("click", async () => {
    const url = document.getElementById("youtubeUrl").value;

    if (url === "") {
        alert("Please paste a YouTube link");
        return;
    }

    output.innerHTML = "<p>⏳ Processing lecture...</p>";

    // Dummy backend call (structure real hai)
    try {
        const response = await fetch("https://your-backend-url/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                youtube_url: url
            })
        });

        // ⚠️ Abhi real call nahi ho raha
        // Isliye hum dummy data use kar rahe hain
        const data = {
            message: "Lecture processed successfully",
            notes: "This is a sample Hinglish note generated from the lecture.",
            quiz: [
                {
                    question: "What is the main topic of the lecture?",
                    options: ["Option A", "Option B", "Option C", "Option D"]
                }
            ]
        };

        renderResult(data);

    } catch (error) {
        output.innerHTML = "<p>❌ Something went wrong.</p>";
    }
});

function renderResult(data) {
    let html = `
        <h3>✅ ${data.message}</h3>
        <h4>📘 Notes</h4>
        <p>${data.notes}</p>
        <h4>❓ Quiz</h4>
    `;

    data.quiz.forEach((q, index) => {
        html += `<p><strong>Q${index + 1}:</strong> ${q.question}</p>`;
        q.options.forEach(opt => {
            html += `<li>${opt}</li>`;
        });
    });

    output.innerHTML = html;
}
