const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const serviceCards = document.querySelectorAll("[data-service]");
const contextPill = document.getElementById("context-pill");
const openChatButtons = document.querySelectorAll("[data-open-chat]");
const welcomePage = document.getElementById("welcome-page");
const assistantPanel = document.getElementById("assistant-panel");
const pageTransitionMs = 340;

function showAssistantPage() {
    if (!welcomePage || !assistantPanel) {
        return;
    }

    welcomePage.classList.remove("is-active");

    window.setTimeout(() => {
        welcomePage.hidden = true;
        assistantPanel.hidden = false;
        window.scrollTo(0, 0);
        window.requestAnimationFrame(() => {
            assistantPanel.classList.add("is-active");
            scrollChatToBottom();
        });
    }, pageTransitionMs);
}

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
    questionInput.style.height = `${Math.min(questionInput.scrollHeight, 150)}px`;
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

serviceCards.forEach((card) => {
    card.addEventListener("click", () => {
        serviceCards.forEach((item) => item.classList.remove("is-selected"));
        card.classList.add("is-selected");

        if (contextPill) {
            contextPill.textContent = card.dataset.service || "Banking guidance";
        }

        if (questionInput) {
            questionInput.value = card.dataset.prompt || "";
            autoResizeTextarea();
            questionInput.focus();
        }
    });
});

openChatButtons.forEach((button) => {
    button.addEventListener("click", () => {
        if (questionInput) {
            questionInput.value = button.dataset.fillQuestion || "";
            autoResizeTextarea();
        }

        showAssistantPage();

        if (questionInput) {
            window.setTimeout(() => questionInput.focus(), pageTransitionMs + 80);
        }
    });
});
