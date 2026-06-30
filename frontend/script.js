/* ============================================================
   SR-71 BLACKBIRD AI — Frontend Logic
   ============================================================ */

(function () {
    'use strict';

    // ── DOM References ───────────────────────────────────────
    const chatMessages  = document.getElementById('chatMessages');
    const chatForm      = document.getElementById('chatForm');
    const chatInput     = document.getElementById('chatInput');
    const sendBtn       = document.getElementById('sendBtn');
    const welcomeCard   = document.getElementById('welcomeCard');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // ── State ────────────────────────────────────────────────
    let isWaiting = false;

    // ── Auto-resize Textarea ─────────────────────────────────
    function autoResize() {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
    }

    chatInput.addEventListener('input', () => {
        autoResize();
        sendBtn.disabled = chatInput.value.trim().length === 0;
    });

    // ── Send on Enter (Shift+Enter = newline) ────────────────
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isWaiting && chatInput.value.trim()) {
                chatForm.requestSubmit();
            }
        }
    });

    // ── Suggestion Chips ─────────────────────────────────────
    suggestionChips.forEach((chip) => {
        chip.addEventListener('click', () => {
            const question = chip.getAttribute('data-question');
            if (question && !isWaiting) {
                chatInput.value = question;
                sendBtn.disabled = false;
                autoResize();
                chatForm.requestSubmit();
            }
        });
    });

    // ── Form Submit ──────────────────────────────────────────
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question || isWaiting) return;

        // Hide welcome card on first message
        if (welcomeCard) {
            welcomeCard.classList.add('hidden');
        }

        // Append user bubble
        appendMessage('user', question);

        // Clear input
        chatInput.value = '';
        sendBtn.disabled = true;
        autoResize();

        // Show typing indicator
        const typingEl = showTypingIndicator();

        // Lock input
        isWaiting = true;
        chatInput.setAttribute('disabled', '');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json();
            removeTypingIndicator(typingEl);
            appendMessage('assistant', data.answer);
        } catch (err) {
            removeTypingIndicator(typingEl);
            appendMessage(
                'assistant',
                'Sorry, something went wrong. Please try again.',
                true
            );
            console.error('Chat error:', err);
        } finally {
            isWaiting = false;
            chatInput.removeAttribute('disabled');
            chatInput.focus();
        }
    });

    // ── Append a Message Bubble ──────────────────────────────
    function appendMessage(role, text, isError = false) {
        const row = document.createElement('div');
        row.className = `message-row ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.textContent = role === 'user' ? 'U' : 'AI';

        const bubble = document.createElement('div');
        bubble.className = 'msg-bubble';
        if (isError) bubble.classList.add('error-bubble');

        if (role === 'assistant') {
            bubble.innerHTML = renderMarkdown(text);
        } else {
            bubble.textContent = text;
        }

        row.appendChild(avatar);
        row.appendChild(bubble);
        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // ── Simple Markdown Renderer ─────────────────────────────
    function renderMarkdown(text) {
        if (!text) return '';

        let html = escapeHtml(text);

        // Bold: **text**
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // Italic: *text*
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Inline code: `code`
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Unordered list items: - item or * item (at start of line)
        html = html.replace(/^[\-\*]\s+(.+)$/gm, '<li>$1</li>');

        // Ordered list items: 1. item
        html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

        // Wrap consecutive <li> in <ul>
        html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');

        // Paragraphs: split by double newlines
        html = html
            .split(/\n{2,}/)
            .map((block) => {
                block = block.trim();
                if (!block) return '';
                // Don't wrap blocks already in tags
                if (/^<(ul|ol|li|h|p|div|blockquote)/i.test(block)) return block;
                return `<p>${block}</p>`;
            })
            .join('');

        // Single newlines inside <p> → <br>
        html = html.replace(/<p>([\s\S]*?)<\/p>/g, (_, inner) => {
            return `<p>${inner.replace(/\n/g, '<br>')}</p>`;
        });

        return html;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ── Typing Indicator ─────────────────────────────────────
    function showTypingIndicator() {
        const wrapper = document.createElement('div');
        wrapper.className = 'typing-indicator';
        wrapper.id = 'typingIndicator';

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.textContent = 'AI';

        const dots = document.createElement('div');
        dots.className = 'typing-dots';
        dots.innerHTML = '<span></span><span></span><span></span>';

        wrapper.appendChild(avatar);
        wrapper.appendChild(dots);
        chatMessages.appendChild(wrapper);
        scrollToBottom();
        return wrapper;
    }

    function removeTypingIndicator(el) {
        if (el && el.parentNode) {
            el.parentNode.removeChild(el);
        }
    }

    // ── Auto-scroll ──────────────────────────────────────────
    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // ── Focus input on load ──────────────────────────────────
    chatInput.focus();
})();
