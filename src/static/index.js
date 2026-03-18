document.addEventListener('DOMContentLoaded', () => {
    const logBoxes = document.querySelectorAll('.container-log-box');

    logBoxes.forEach(box => {
        const pre = box.querySelector('pre');
        if (!pre) return;

        // 1. Hook into the toggle event for the initial jump
        box.addEventListener('toggle', () => {
            if (box.open) {
                pre.scrollTop = pre.scrollHeight;
            }
        });

        // 2. Create an observer to watch for text changes (Sticky Logic)
        const observer = new MutationObserver(() => {
            // Only auto-scroll if the box is currently open
            if (box.open) {
                pre.scrollTop = pre.scrollHeight;
            }
        });

        // Start observing the <pre> tag for character changes or new child elements
        observer.observe(pre, { 
            childList: true, 
            characterData: true, 
            subtree: true 
        });
    });
});