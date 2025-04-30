document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");
    const micBtn = document.getElementById("micBtn");
    const fileUpload = document.getElementById("fileUpload");
    const exportPdfBtn = document.getElementById("exportPdfBtn");
  
    function addMessage(content, sender = 'bot') {
      const messageWrapper = document.createElement("div");
      messageWrapper.classList.add(sender === 'user' ? "user-message" : "bot-message");
  
      const messageContent = document.createElement("div");
      messageContent.classList.add("message-content");
  
      if (sender === "bot") {
        messageContent.innerHTML = marked.parse(content);
      } else {
        messageContent.textContent = content;
      }
  
      // Add controls
      const controls = document.createElement("div");
      controls.className = "message-controls";
  
      const copyBtn = document.createElement("button");
      copyBtn.innerText = "📋";
      copyBtn.title = "Copy message";
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(messageContent.innerText);
      };
  
      const editBtn = document.createElement("button");
      editBtn.innerText = "✏️";
      editBtn.title = "Edit message";
      editBtn.onclick = () => {
        const newText = prompt("Edit message:", messageContent.innerText);
        if (newText !== null) {
          if (sender === "bot") {
            messageContent.innerHTML = marked.parse(newText);
          } else {
            messageContent.textContent = newText;
          }
        }
      };
  
      controls.appendChild(copyBtn);
      controls.appendChild(editBtn);
  
      messageWrapper.appendChild(messageContent);
      messageWrapper.appendChild(controls);
      chatBox.appendChild(messageWrapper);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    function sendMessage() {
      const message = userInput.value.trim();
      if (message !== "") {
        addMessage(message, "user");
        fetch("/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
          addMessage(data.reply, "bot");
        })
        .catch(() => {
          addMessage("Error processing your request.", "bot");
        });
        userInput.value = "";
      }
    }
  
    sendBtn.addEventListener("click", sendMessage);
  
    userInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  
    micBtn.addEventListener("click", function () {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      recognition.lang = "en-US";
      recognition.start();
  
      recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage();
      };
  
      recognition.onerror = function () {
        alert("Voice recognition failed. Try again.");
      };
    });
  
    fileUpload.addEventListener("change", function () {
      const file = fileUpload.files[0];
      const formData = new FormData();
      formData.append("file", file);
  
      fetch("/upload", {
        method: "POST",
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        addMessage(data.message, "bot");
      })
      .catch(() => {
        addMessage("Failed to upload file.", "bot");
      });
    });
  
    exportPdfBtn.addEventListener("click", function () {
      const element = document.createElement('a');
      const blob = new Blob([chatBox.innerText], { type: 'application/pdf' });
      element.href = URL.createObjectURL(blob);
      element.download = "chat_export.pdf";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    });
  });
  