class VirtualJoystick {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.size = options.size || 150;
        this.maxDistance = options.maxDistance || 50;
        this.zone = this.createZone();
        this.position = { x: 0, y: 0 };
        this.normalized = { x: 0, y: 0 };
        this.onChange = options.onChange || (() => {});
        
        this.initJoystick();
    }

    createZone() {
        const zone = document.createElement('div');
        zone.className = 'joystick-zone';
        zone.style.width = `${this.size}px`;
        zone.style.height = `${this.size}px`;
        this.container.appendChild(zone);
        return zone;
    }

    initJoystick() {
        let isDragging = false;
        const stick = document.createElement('div');
        stick.className = 'joystick-stick';
        this.zone.appendChild(stick);

        const handleMove = (e) => {
            if (!isDragging) return;

            const rect = this.zone.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            let x = (e.type === 'touchmove' ? e.touches[0].clientX : e.clientX) - centerX;
            let y = (e.type === 'touchmove' ? e.touches[0].clientY : e.clientY) - centerY;

            // Calculate distance from center
            const distance = Math.sqrt(x * x + y * y);
            if (distance > this.maxDistance) {
                const angle = Math.atan2(y, x);
                x = Math.cos(angle) * this.maxDistance;
                y = Math.sin(angle) * this.maxDistance;
            }

            // Update stick position
            stick.style.transform = `translate(${x}px, ${y}px)`;

            // Normalize values to -1 to 1
            this.normalized.x = x / this.maxDistance;
            this.normalized.y = -y / this.maxDistance; // Invert Y for intuitive controls
            this.onChange(this.normalized);
        };

        const handleStart = (e) => {
            isDragging = true;
            handleMove(e);
        };

        const handleEnd = () => {
            isDragging = false;
            stick.style.transform = 'translate(0px, 0px)';
            this.normalized = { x: 0, y: 0 };
            this.onChange(this.normalized);
        };

        // Mouse events
        this.zone.addEventListener('mousedown', handleStart);
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', handleEnd);

        // Touch events
        this.zone.addEventListener('touchstart', handleStart);
        document.addEventListener('touchmove', handleMove);
        document.addEventListener('touchend', handleEnd);
    }
}
