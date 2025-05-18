    const grid = document.querySelector('.grid');
    const cols = Math.ceil(window.innerWidth / 40);
    const rows = Math.ceil(window.innerHeight / 40);
    const centerX = cols / 2;
    const centerY = rows / 2;

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
        const dot = document.createElement('div');
        dot.className = 'grid-dot';

        const dx = x - centerX;
        const dy = y - centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const delay = distance * 0.1; // tune the speed of wave
        dot.style.animationDelay = `${delay}s`;

        grid.appendChild(dot);
        }
    }