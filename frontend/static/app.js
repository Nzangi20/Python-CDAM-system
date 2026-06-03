document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initMobileMenu();
  initTabs();
  initCodeBlocks();
  initToasts();
  initChatbot();
  initAIAssistant();
  initScrollReveal();
  initStatsCounters();
  initActiveNav();
  if (window.hljs) {
    document.querySelectorAll("pre code").forEach((block) => hljs.highlightElement(block));
  }
});

function initActiveNav() {
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach((a) => {
    if (a.getAttribute("href") === currentPath) {
      a.classList.add("active");
    }
  });
}

function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("reveal-visible");
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(".card, .stat-card, .hero, .quiz-item").forEach((el) => {
    el.classList.add("reveal-item");
    observer.observe(el);
  });
}

function initStatsCounters() {
  const counters = document.querySelectorAll(".stat-card p");
  counters.forEach((counter) => {
    const text = counter.textContent.trim();
    // Only animate clean integers
    if (/^\d+$/.test(text)) {
      const target = parseInt(text, 10);
      if (target === 0) return;
      let current = 0;
      const step = Math.ceil(target / 40);
      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          counter.textContent = target;
          clearInterval(timer);
        } else {
          counter.textContent = current;
        }
      }, 25);
    }
  });
}

function initTheme() {
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");
  const saved = localStorage.getItem("cdam-theme") || "light";
  root.setAttribute("data-theme", saved);
  toggle?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("cdam-theme", next);
  });
}

function initMobileMenu() {
  const toggle = document.getElementById("menuToggle");
  const nav = document.getElementById("navLinks");
  toggle?.addEventListener("click", () => nav?.classList.toggle("open"));
}

function initTabs() {
  const tabs = document.querySelectorAll(".tab");
  const panels = document.querySelectorAll(".tab-panel");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.tab;
      tabs.forEach((t) => t.classList.remove("active"));
      panels.forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(target)?.classList.add("active");
    });
  });
}

function switchTab(tabId) {
  const tabButton = document.querySelector(`.tab[data-tab="${tabId}"]`);
  if (tabButton) {
    tabButton.click();
    const tabsContainer = document.querySelector(".tabs");
    if (tabsContainer) {
      tabsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
}
window.switchTab = switchTab;

function initCodeBlocks() {
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const code = btn.dataset.copy || "";
      await navigator.clipboard.writeText(code);
      showToast("Code copied to clipboard.", "success");
    });
  });

  const btnRun = document.getElementById("btnRunCode");
  const codeEditor = document.getElementById("codeEditor");
  const output = document.getElementById("runOutput");
  const outputText = document.getElementById("runOutputText");
  const btnReset = document.getElementById("btnResetCode");

  if (btnRun && codeEditor && output && outputText) {
    const originalCode = codeEditor.value;

    btnRun.addEventListener("click", async () => {
      const code = codeEditor.value;
      output.hidden = false;
      outputText.textContent = ">>> Executing script inside sandbox, please wait...\n";
      
      try {
        btnRun.disabled = true;
        btnRun.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running...';
        
        const response = await fetch("/api/run-code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code })
        });
        const data = await response.json();
        
        if (data.error) {
          outputText.textContent = (data.output ? data.output + "\n" : "") + "--- ERROR ---\n" + data.error;
          showToast("Code completed with error.", "error");
          if (window.triggerAIDebugger) {
            window.triggerAIDebugger(data.error);
          }
        } else {
          outputText.textContent = data.output || ">>> Execution finished (no standard output to show).";
          showToast("Execution completed successfully.", "success");
          if (window.triggerAISuccessSuggestion) {
            window.triggerAISuccessSuggestion();
          }
        }
      } catch (err) {
        outputText.textContent = ">>> Error: Failed to contact the backend code sandbox. " + err;
        showToast("Backend connection failed.", "error");
      } finally {
        btnRun.disabled = false;
        btnRun.innerHTML = '<i class="fa-solid fa-play"></i> Run Code';
      }
    });

    if (btnReset) {
      btnReset.addEventListener("click", () => {
        codeEditor.value = originalCode;
        showToast("Editor reset to original lesson example.", "success");
      });
    }
  }

  document.querySelectorAll(".run-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const code = btn.dataset.code || "";
      const out = document.getElementById("runOutput");
      const outText = document.getElementById("runOutputText");
      if (!out || !outText) return;
      out.hidden = false;
      outText.textContent = simulatePython(code);
      showToast("Code simulation completed.", "success");
    });
  });
}

function simulatePython(code) {
  const lines = [];
  lines.push(">>> Running CDAM code simulation...");
  if (code.includes("print(")) {
    const matches = [...code.matchAll(/print\((.*?)\)/gs)];
    matches.forEach((match) => {
      let value = match[1].trim();
      if ((value.startsWith("'") && value.endsWith("'")) || (value.startsWith('"') && value.endsWith('"'))) {
        value = value.slice(1, -1);
      }
      lines.push(value);
    });
  }
  if (code.includes("describe()")) lines.push("       a          b\ncount  2.000000  2.000000\nmean   1.500000  3.500000");
  if (code.includes("accuracy_score") || code.includes("Accuracy:")) lines.push("Accuracy: 1.0");
  if (code.includes("rolling")) lines.push("2024-03-31    131.0\n2024-04-30    144.0\n2024-05-31    160.7");
  if (lines.length === 1) lines.push("Simulation finished successfully.");
  return lines.join("\n");
}

function initToasts() {
  document.querySelectorAll("[data-toast]").forEach((node) => {
    showToast(node.textContent.trim(), node.classList.contains("error") ? "error" : "success");
    node.remove();
  });
}

function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

function initChatbot() {
  const toggle = document.getElementById("chatbotToggle");
  const panel = document.getElementById("chatbotPanel");
  const close = document.getElementById("chatbotClose");
  const form = document.getElementById("chatbotForm");
  const input = document.getElementById("chatbotInput");
  const messages = document.getElementById("chatbotMessages");

  toggle?.addEventListener("click", () => panel?.classList.add("open"));
  close?.addEventListener("click", () => panel?.classList.remove("open"));

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    appendChat(messages, message, "user");
    input.value = "";
    try {
      const response = await fetch("/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      appendChat(messages, data.reply || "I am here to help with CDAM learning.", "bot");
    } catch {
      appendChat(messages, "Assistant is temporarily unavailable.", "bot");
    }
  });
}

function appendChat(container, text, role) {
  const node = document.createElement("div");
  node.className = role === "user" ? "user-msg" : "bot-msg";
  node.textContent = text;
  container.appendChild(node);
  container.scrollTop = container.scrollHeight;
}

function initAIAssistant() {
  const panel = document.getElementById("code");
  if (!panel) return;
  const sessionId = panel.dataset.sessionId;
  if (!sessionId) return;

  const chatMessages = document.getElementById("aiChatMessages");
  const chatForm = document.getElementById("aiChatForm");
  const chatInput = document.getElementById("aiChatInput");
  const codeEditor = document.getElementById("codeEditor");

  // Handle Action Pills
  document.querySelectorAll(".ai-action-pill").forEach(pill => {
    pill.addEventListener("click", async () => {
      const action = pill.dataset.action;
      const code = codeEditor ? codeEditor.value : "";
      
      appendChatBubble(chatMessages, `AI Coach, please run a code ${action} check.`, "user");
      
      const botLoading = appendChatBubble(chatMessages, "🤖 AI Coach is typing...", "bot");
      
      try {
        const response = await fetch("/api/ai-assistant", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, code, action })
        });
        const data = await response.json();
        botLoading.innerHTML = `<strong>🤖 AI Coach:</strong> ${formatMarkdown(data.reply)}`;
      } catch (err) {
        botLoading.textContent = "AI Tutor is temporarily offline.";
      }
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
  });

  // Handle Form Submission
  chatForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    appendChatBubble(chatMessages, query, "user");
    chatInput.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const code = codeEditor ? codeEditor.value : "";
    const botLoading = appendChatBubble(chatMessages, "🤖 AI Coach is typing...", "bot");

    try {
      const response = await fetch("/api/ai-assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, code, query, action: "chat" })
      });
      const data = await response.json();
      botLoading.innerHTML = `<strong>🤖 AI Coach:</strong> ${formatMarkdown(data.reply)}`;
    } catch (err) {
      botLoading.textContent = "AI Tutor is temporarily offline.";
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  });

  window.triggerAIDebugger = async (errorText) => {
    if (!chatMessages) return;
    appendChatBubble(chatMessages, "🚨 Code failed with an execution error.", "user");
    const botLoading = appendChatBubble(chatMessages, "🤖 AI Debugger is analyzing...", "bot");
    try {
      const response = await fetch("/api/ai-assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, code: codeEditor.value, action: "debug", error: errorText })
      });
      const data = await response.json();
      botLoading.innerHTML = `<strong>🤖 AI Coach:</strong> ${formatMarkdown(data.reply)}`;
    } catch {
      botLoading.textContent = "AI Tutor is temporarily offline.";
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  window.triggerAISuccessSuggestion = async () => {
    if (!chatMessages) return;
    appendChatBubble(chatMessages, "✅ Code executed successfully.", "user");
    const botLoading = appendChatBubble(chatMessages, "🤖 AI Coach is reviewing...", "bot");
    try {
      const response = await fetch("/api/ai-assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, code: codeEditor.value, action: "review" })
      });
      const data = await response.json();
      
      const challengeResponse = await fetch("/api/ai-assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, code: codeEditor.value, action: "challenge" })
      });
      const challengeData = await challengeResponse.json();
      
      botLoading.innerHTML = `<strong>🤖 AI Coach:</strong> Excellent! Here is my feedback and your next challenge:<br><br>${formatMarkdown(data.reply)}<br><br>${formatMarkdown(challengeData.reply)}`;
    } catch {
      botLoading.textContent = "AI Tutor is temporarily offline.";
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };
}

function appendChatBubble(container, text, role) {
  if (!container) return null;
  const bubble = document.createElement("div");
  if (role === "user") {
    bubble.className = "user-msg";
    bubble.style.cssText = "align-self: flex-end; background: var(--purple-brand); color: #ffffff; border-radius: 8px 8px 0 8px; padding: 0.65rem 0.85rem; font-size: 0.875rem; max-width: 90%; margin-bottom: 0.5rem;";
    bubble.textContent = text;
  } else {
    bubble.className = "bot-msg";
    bubble.style.cssText = "padding: 0.65rem 0.85rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px 8px 8px 0; font-size: 0.875rem; align-self: flex-start; max-width: 90%; margin-bottom: 0.5rem;";
    bubble.innerHTML = `<strong>🤖 AI Coach:</strong> ${text}`;
  }
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
  return bubble;
}

function formatMarkdown(text) {
  if (!text) return "";
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, "<code style='background: rgba(0,0,0,0.1); padding: 2px 4px; border-radius: 4px; font-family: monospace;'>$1</code>")
    .replace(/\n/g, "<br>");
  return formatted;
}
