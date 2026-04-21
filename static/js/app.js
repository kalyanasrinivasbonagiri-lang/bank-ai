const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const promptChips = document.querySelectorAll("[data-prompt]");

function scrollChatToBottom() {
    if (!chatLog) {
        return;
    }
    chatLog.scrollTop = chatLog.scrollHeight;
}

function autoResizeTextarea() {
    if (!questionInput) {
        return;
    }
    questionInput.style.height = "auto";
    questionInput.style.height = `${Math.min(questionInput.scrollHeight, 220)}px`;
}

if (chatLog) {
    scrollChatToBottom();
}

if (questionInput) {
    autoResizeTextarea();

    questionInput.addEventListener("input", autoResizeTextarea);
    questionInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            if (chatForm) {
                chatForm.submit();
            }
        }
    });
}

promptChips.forEach((chip) => {
    chip.addEventListener("click", () => {
        if (!questionInput) {
            return;
        }
        questionInput.value = chip.dataset.prompt || "";
        autoResizeTextarea();
        questionInput.focus();
    });
});
