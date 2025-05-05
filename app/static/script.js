const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

function appendUserMessage(content) {
  const msgDiv = document.createElement("div");
  msgDiv.className = "msg user";
  msgDiv.textContent = content;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.onsubmit = async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  appendUserMessage(message);
  userInput.value = "";

  const msgDiv = document.createElement("div");
  msgDiv.className = "msg bot";
  const card = document.createElement("div");
  card.className = "bot-msg-card";
  msgDiv.appendChild(card);
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  const steps = data.response.split(/\n+/);

  for (let step of steps) {
    if (step.trim()) {
      const line = document.createElement("div");
      line.innerText = step.trim();
      card.appendChild(line);
      chatBox.scrollTop = chatBox.scrollHeight;
      await new Promise(resolve => setTimeout(resolve, 600));
    }
  }

  if (data.image_url) {
    const img = document.createElement("img");
    img.src = data.image_url;
    img.alt = "Generated goal visual";
    img.style.marginTop = "12px";
    img.style.borderRadius = "10px";
    img.style.maxWidth = "100%";
    chatBox.appendChild(img);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
};
