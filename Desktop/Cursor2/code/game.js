// --- Helper for animation ---
function lerp(a, b, t) { return a + (b - a) * t; }

class LensPuzzle {
    constructor() {
        this.canvas = document.getElementById('puzzleCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.moves = 0;
        this.timer = 0;
        this.timerInterval = null;
        this.isPlaying = false;
        this.gridSize = 3;
        this.tileSize = 0;
        this.tiles = [];
        this.selectedTile = null;
        this.image = new Image();
        this.image.src = 'puzzle-image.png'; // Use your own image or replace with a placeholder
        this.animating = false;
        this.animationTiles = [];
        this.animationStart = 0;
        this.animationDuration = 200; // ms
        this.particles = [];
        this.hintTimeout = null;

        // DOM elements
        this.movesElement = document.getElementById('moves');
        this.timerElement = document.getElementById('timer');
        this.shuffleBtn = document.getElementById('shuffleBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.difficultySelect = document.getElementById('difficulty');
        this.winModal = document.getElementById('winModal');
        this.finalMovesElement = document.getElementById('finalMoves');
        this.finalTimeElement = document.getElementById('finalTime');
        this.playAgainBtn = document.getElementById('playAgainBtn');
        this.hintBtn = document.getElementById('hintBtn');
        this.hintOverlay = document.getElementById('hintOverlay');

        // Touch support
        this.touchStart = null;
        this.touchMoved = false;

        // Bind event listeners
        this.shuffleBtn.addEventListener('click', () => this.shuffle());
        this.resetBtn.addEventListener('click', () => this.reset());
        this.difficultySelect.addEventListener('change', (e) => this.setDifficulty(e.target.value));
        this.playAgainBtn.addEventListener('click', () => this.reset());
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        this.canvas.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: false });
        this.canvas.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        this.canvas.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: false });
        this.hintBtn.addEventListener('click', () => this.showHint());
        this.hintOverlay.addEventListener('click', () => this.hideHint());

        // Initialize
        this.image.onload = () => {
            this.initialize();
        };
        this.image.onerror = () => {
            alert('Failed to load image. Please check the image path.');
        };
    }

    initialize() {
        this.canvas.width = Math.min(500, window.innerWidth - 40);
        this.canvas.height = this.canvas.width;
        this.tileSize = this.canvas.width / this.gridSize;
        this.createTiles();
        this.draw();
    }

    createTiles() {
        this.tiles = [];
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                // Add random rotation (0, 90, 180, 270)
                const rotation = Math.floor(Math.random() * 4) * 90;
                this.tiles.push({
                    x: x,
                    y: y,
                    correctX: x,
                    correctY: y,
                    rotation: rotation
                });
            }
        }
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        // Calculate image fit (cover)
        const imgAspect = this.image.width / this.image.height;
        const canvasAspect = this.canvas.width / this.canvas.height;
        let sx, sy, sWidth, sHeight;
        if (imgAspect > canvasAspect) {
            sHeight = this.image.height;
            sWidth = sHeight * canvasAspect;
            sx = (this.image.width - sWidth) / 2;
            sy = 0;
        } else {
            sWidth = this.image.width;
            sHeight = sWidth / canvasAspect;
            sx = 0;
            sy = (this.image.height - sHeight) / 2;
        }
        // Draw tiles
        this.tiles.forEach((tile, idx) => {
            let drawX = tile.x * this.tileSize;
            let drawY = tile.y * this.tileSize;
            // Animation
            if (tile.animating) {
                drawX = lerp(tile.fromX, tile.x * this.tileSize, tile.animT);
                drawY = lerp(tile.fromY, tile.y * this.tileSize, tile.animT);
            }
            this.ctx.save();
            this.ctx.globalAlpha = 0.8;
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
            this.ctx.fillRect(drawX, drawY, this.tileSize, this.tileSize);
            this.ctx.restore();
            // Draw rotated image portion
            this.ctx.save();
            this.ctx.translate(drawX + this.tileSize/2, drawY + this.tileSize/2);
            this.ctx.rotate((tile.rotation || 0) * Math.PI / 180);
            this.ctx.drawImage(
                this.image,
                sx + tile.correctX * sWidth / this.gridSize,
                sy + tile.correctY * sHeight / this.gridSize,
                sWidth / this.gridSize,
                sHeight / this.gridSize,
                -this.tileSize/2,
                -this.tileSize/2,
                this.tileSize,
                this.tileSize
            );
            this.ctx.restore();
        });
    }

    // ... (rest of the LensPuzzle class as in previous version)
}

window.addEventListener('load', () => {
    new LensPuzzle();
}); 