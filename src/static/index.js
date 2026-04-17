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


    chain.forEach((block, index) => {
        const div = document.createElement('div');
        div.className = 'chain-entry';

        div.innerHTML = `
            <p>
                <div style="padding-bottom: 2px; margin-bottom: 4px; font-weight: bold;">
                    ${block.timestamp}
                </div>
                Hash: ${block.block_hash}<br>
                Prev: ${block.previous_hash}<br>
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

function showContainerLogs(containerName) {
    const logContent = document.getElementById('log-content');

    if (!window.currentBlock) return;

    const logs = window.currentBlock.logs[containerName] || "No logs";

    logContent.innerHTML = `
        <button onclick="loadLogs(window.currentBlock)">⬅ Back</button>
        <h3>${containerName}</h3>
        <pre>${logs}</pre>
    `;
}

function loadLogs(block) {
    const logContent = document.getElementById('log-content');

    if (!logContent) return;

    let html = "";
    for (const container in block.logs) {
        html += `
            <div class="container-entry" onclick="showContainerLogs('${container}')">
                ${container}
            </div>
        `;
    }

    logContent.innerHTML = html;

    // store current block globally
    window.currentBlock = block;
}

// ===============================
// RUN AFTER PAGE LOAD
// ===============================
window.addEventListener('DOMContentLoaded', () => {
    loadChain();
    setInterval(loadChain, 60000);
});
