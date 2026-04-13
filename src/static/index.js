// ===============================
// EXISTING LOG AUTO-SCROLL LOGIC
// ===============================
document.addEventListener('DOMContentLoaded', () => {
    const logBoxes = document.querySelectorAll('.container-log-box');

    logBoxes.forEach(box => {
        const pre = box.querySelector('pre');
        if (!pre) return;

        box.addEventListener('toggle', () => {
            if (box.open) {
                pre.scrollTop = pre.scrollHeight;
            }
        });

        const observer = new MutationObserver(() => {
            if (box.open) {
                pre.scrollTop = pre.scrollHeight;
            }
        });

        observer.observe(pre, { 
            childList: true, 
            characterData: true, 
            subtree: true 
        });
    });
});


// ===============================
// NEW BLOCKCHAIN LOGIC
// ===============================

async function loadChain() {
    console.log("Loading chain...");

    const res = await fetch('/api/chain/');
    const chain = await res.json();

    console.log("CHAIN:", chain);

    const chainPanel = document.getElementById('chain-panel');
    if (!chainPanel) {
        console.error("chain-panel not found");
        return;
    }

    chainPanel.innerHTML = '';

    if (chain.length === 0) {
        chainPanel.innerHTML = "<p>No chain data yet</p>";
        return;
    }

    chain.reverse();

    chain.forEach((block, index) => {
        const div = document.createElement('div');
        div.className = 'chain-entry';

        div.innerHTML = `
            <p>
                <strong>Block ${index + 1}</strong><br>
                Hash: ${block.block_hash.substring(0, 16)}...<br>
                Prev: ${block.previous_hash.substring(0, 16)}...<br>
                Time: ${block.timestamp}
            </p>
        `;

        div.onclick = () => {
            const isSame = currentBlockHash === block.block_hash;

            // remove all highlights first
            document.querySelectorAll('.chain-entry').forEach(e => {
                e.classList.remove('active');
            });

            // toggle behavior
            if (isSame) {
                loadLogs(block); // this will clear logs
            } else {
                div.classList.add('active');
                loadLogs(block);
            }
        };

        chainPanel.appendChild(div);
    });
}

let currentBlockHash = null;

function loadLogs(block) {
    const logContent = document.getElementById('log-content');

    // 🔁 If clicking same block again → clear logs
    if (currentBlockHash === block.block_hash) {
        logContent.innerHTML = "<p>Select a block to view logs.</p>";
        currentBlockHash = null;
        return;
    }

    // otherwise show logs
    currentBlockHash = block.block_hash;

    let logsText = "";

    for (const [container, log] of Object.entries(block.logs)) {
        logsText += `=== ${container} ===\n${log}\n\n`;
    }

    logContent.innerHTML = `<pre>${logsText}</pre>`;
}

// ===============================
// RUN AFTER PAGE LOAD
// ===============================
window.addEventListener('DOMContentLoaded', () => {
    loadChain();
    setInterval(loadChain, 5000);
});