document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initMobileMenu();
  initTabs();
  initCodeBlocks();
  initToasts();
  initAIPanel();
  initSandboxFiles();
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
        } else {
          outputText.textContent = data.output || ">>> Execution finished (no standard output to show).\n\nHint: Use the print() function to display results, values, or dataframe contents in the console.\nExample: print(df.head())";
          showToast("Execution completed successfully.", "success");
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



/* ===================================================================
   AI LEARNING ASSISTANT PANEL (Gemini-powered)
   =================================================================== */

function initAIPanel() {
  const aiPanel = document.getElementById("ai-assistant");
  if (!aiPanel) return;

  const sessionId = aiPanel.dataset.sessionId;
  if (!sessionId) return;

  const responseContent = document.getElementById("aiResponseContent");
  const responseCard = document.getElementById("aiResponseCard");
  const copyBtn = document.getElementById("aiCopyBtn");
  const chatForm = document.getElementById("aiPanelChatForm");
  const chatInput = document.getElementById("aiPanelChatInput");
  const codeEditor = document.getElementById("codeEditor");
  const datasetInput = document.getElementById("datasetUpload");

  let lastRawResponse = "";

  // --- Action Buttons ---
  document.querySelectorAll(".ai-action-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const action = btn.dataset.aiAction;
      if (!action) return;

      const code = codeEditor ? codeEditor.value : "";
      const outputText = document.getElementById("runOutputText");
      const lastError = outputText ? outputText.textContent : "";

      let endpoint = `/api/ai/${action}`;
      let body = { session_id: sessionId, code };

      // For explain-error, include the last error
      if (action === "explain-error") {
        body.error = lastError;
      }

      showAILoading(responseContent, copyBtn);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        const data = await response.json();
        lastRawResponse = data.reply || "";
        renderAIResponse(responseContent, copyBtn, data.reply);
      } catch (err) {
        renderAIResponse(responseContent, copyBtn, "AI service is temporarily unavailable. Please try again.");
      }
    });
  });

  // --- Dataset Upload ---
  if (datasetInput) {
    datasetInput.addEventListener("change", async () => {
      const file = datasetInput.files[0];
      if (!file) return;

      showAILoading(responseContent, copyBtn);

      const formData = new FormData();
      formData.append("session_id", sessionId);
      formData.append("dataset", file);

      try {
        const response = await fetch("/api/ai/analyze-dataset", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        lastRawResponse = data.reply || "";
        renderAIResponse(responseContent, copyBtn, data.reply);
      } catch (err) {
        renderAIResponse(responseContent, copyBtn, "Failed to analyze dataset. Please try again.");
      }
      datasetInput.value = "";
    });
  }

  // --- Free-form Chat ---
  chatForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;
    chatInput.value = "";

    const code = codeEditor ? codeEditor.value : "";

    showAILoading(responseContent, copyBtn);

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, query, code }),
      });
      const data = await response.json();
      lastRawResponse = data.reply || "";
      renderAIResponse(responseContent, copyBtn, data.reply);
    } catch (err) {
      renderAIResponse(responseContent, copyBtn, "AI service is temporarily unavailable. Please try again.");
    }
  });

  // --- Copy Button ---
  copyBtn?.addEventListener("click", async () => {
    if (lastRawResponse) {
      await navigator.clipboard.writeText(lastRawResponse);
      showToast("AI response copied to clipboard.", "success");
    }
  });

  // Auto-trigger hooks for code execution removed to prevent automatic AI generation on run code.
}

function showAILoading(container, copyBtn) {
  if (copyBtn) copyBtn.style.display = "none";
  if (container) {
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; gap: 1rem;">
        <div class="ai-loading">
          <span></span><span></span><span></span>
        </div>
        <p class="muted" style="font-size: 0.9rem;">Gemini AI is thinking...</p>
      </div>
    `;
  }
}

function renderAIResponse(container, copyBtn, text) {
  if (!container) return;
  if (copyBtn) copyBtn.style.display = "inline-flex";
  container.innerHTML = formatAIMarkdown(text || "No response received.");
  // Highlight code blocks if hljs is available
  if (window.hljs) {
    container.querySelectorAll("pre code").forEach((block) => hljs.highlightElement(block));
  }
}

function formatAIMarkdown(text) {
  if (!text) return "";

  // Normalize newlines (CRLF/CR -> LF)
  text = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  const codeBlocks = [];

  // Extract code blocks first to protect them from downstream markdown replacements
  let html = text.replace(/```(\w+)?\n([\s\S]*?)```/g, (_, lang, code) => {
    const placeholder = `<!--CODE_BLOCK_${codeBlocks.length}-->`;
    codeBlocks.push({ lang, code: code.trim() });
    return placeholder;
  });

  html = html
    // Inline code
    .replace(/`([^`]+)`/g, '<code class="ai-inline-code">$1</code>')
    // Headers
    .replace(/^### (.*$)/gm, '<h4 style="font-weight: 700; margin: 1rem 0 0.5rem; font-size: 1.1rem;">$1</h4>')
    .replace(/^## (.*$)/gm, '<h3 style="font-weight: 800; margin: 1.25rem 0 0.5rem; font-size: 1.2rem;">$1</h3>')
    .replace(/^# (.*$)/gm, '<h2 style="font-weight: 800; margin: 1.5rem 0 0.5rem; font-size: 1.3rem;">$1</h2>')
    // Bold
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    // Unordered lists
    .replace(/^- (.*$)/gm, '<li style="margin-left: 1.5rem; margin-bottom: 0.25rem;">$1</li>')
    // Ordered lists
    .replace(/^\d+\. (.*$)/gm, '<li style="margin-left: 1.5rem; margin-bottom: 0.25rem; list-style-type: decimal;">$1</li>')
    // Blockquotes
    .replace(/^> (.*$)/gm, '<blockquote style="border-left: 3px solid var(--purple-brand); padding: 0.5rem 1rem; margin: 0.5rem 0; background: rgba(139, 92, 246, 0.05); border-radius: 0 6px 6px 0;">$1</blockquote>')
    // Tables (simple markdown table support)
    .replace(/\|(.+)\|/g, (match) => {
      const cells = match.split('|').filter(c => c.trim());
      if (cells.every(c => /^[-:]+$/.test(c.trim()))) return '';
      const isHeader = false;
      const tag = isHeader ? 'th' : 'td';
      return '<tr>' + cells.map(c => `<${tag} style="padding: 0.4rem 0.75rem; border: 1px solid var(--border);">${c.trim()}</${tag}>`).join('') + '</tr>';
    })
    // Line breaks for standard text
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>");

  // Wrap in paragraph
  html = `<p>${html}</p>`;

  // Clean up empty elements
  html = html.replace(/<p><\/p>/g, "").replace(/<p><br><\/p>/g, "");

  // Restore the code blocks with preserved spacing and formatting
  codeBlocks.forEach((block, idx) => {
    const placeholder = `<!--CODE_BLOCK_${idx}-->`;
    const langClass = block.lang ? ` class="language-${block.lang}"` : "";
    const restored = `<pre class="ai-code-block"><code${langClass}>${escapeHtml(block.code)}</code></pre>`;
    html = html.replace(placeholder, restored);
  });

  return html;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function initSandboxFiles() {
  const fileInput = document.getElementById("sandboxFileInput");
  const fileNameLabel = document.getElementById("sandboxSelectedFileName");
  const uploadBtn = document.getElementById("sandboxUploadBtn");
  const filesList = document.getElementById("sandboxFilesList");

  if (!fileInput || !filesList) return;

  // Format bytes helper
  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Load and render existing files
  async function loadFiles() {
    try {
      const response = await fetch("/api/sandbox/files");
      const files = await response.json();
      
      if (files.length === 0) {
        filesList.innerHTML = `<p class="muted" style="font-size: 0.85rem; font-style: italic; padding: 0.5rem 0;">No datasets uploaded yet.</p>`;
        return;
      }

      filesList.innerHTML = files.map(file => `
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.02); padding: 0.6rem 1rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.875rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; color: var(--text);">
            <i class="fa-regular fa-file" style="color: var(--purple-brand);"></i>
            <strong style="color: var(--text);">${escapeHtml(file.name)}</strong>
            <span class="muted" style="font-size: 0.775rem;">(${formatBytes(file.size)})</span>
          </div>
          <button class="btn ghost delete-file-btn" data-filename="${encodeURIComponent(file.name)}" style="padding: 0.25rem 0.5rem; color: var(--red-500); hover:background: rgba(239, 68, 68, 0.1);" title="Delete file">
            <i class="fa-regular fa-trash-can"></i>
          </button>
        </div>
      `).join('');

      // Add delete click listeners
      filesList.querySelectorAll(".delete-file-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          const filename = decodeURIComponent(btn.dataset.filename);
          if (confirm(`Are you sure you want to delete "${filename}"?`)) {
            try {
              const res = await fetch(`/api/sandbox/files/${btn.dataset.filename}`, {
                method: "DELETE"
              });
              const resData = await res.json();
              if (resData.success) {
                showToast("File deleted successfully.", "success");
                loadFiles();
              } else {
                showToast(resData.error || "Failed to delete file.", "error");
              }
            } catch (err) {
              showToast("Error deleting file.", "error");
            }
          }
        });
      });
    } catch (err) {
      filesList.innerHTML = `<p class="muted" style="font-size: 0.85rem; color: var(--red-500);">Failed to load files.</p>`;
    }
  }

  // Handle file select change
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      fileNameLabel.textContent = file.name;
      uploadBtn.disabled = false;
    } else {
      fileNameLabel.textContent = "No file chosen";
      uploadBtn.disabled = true;
    }
  });

  // Handle upload button click
  uploadBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    uploadBtn.disabled = true;
    uploadBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Uploading...`;

    try {
      const response = await fetch("/api/sandbox/upload", {
        method: "POST",
        body: formData
      });
      
      const data = await response.json();
      if (response.ok && data.success) {
        showToast("File uploaded successfully to sandbox.", "success");
        fileInput.value = "";
        fileNameLabel.textContent = "No file chosen";
        loadFiles();
      } else {
        showToast(data.error || "Upload failed.", "error");
      }
    } catch (err) {
      showToast("Error uploading file.", "error");
    } finally {
      uploadBtn.disabled = true;
      uploadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-up"></i> Upload File`;
    }
  });

  // Initial load
  loadFiles();
}
