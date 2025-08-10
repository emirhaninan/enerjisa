// Voltage Spike Monitor - Main Application
class VoltageMonitor {
    constructor() {
        this.chart = null;
        this.statusLight = document.getElementById('status-light');
        this.statusText = document.getElementById('status-text');
        this.currentVoltage = document.getElementById('current-voltage');
        this.lastUpdate = document.getElementById('last-update');
        this.spikeAlert = document.getElementById('spike-alert');
        this.telegramNotification = document.getElementById('telegram-notification');
        this.telegramStatus = document.getElementById('telegram-status');
        this.voltageHistory = [];
        this.isSpikeActive = false;
        this.updateInterval = null;
        this.csvData = [];
        this.currentDataIndex = 0;
        
        this.init();
    }
    
    async init() {
        await this.loadCSVData();
        this.setupChart();
        this.startMonitoring();
        this.updateTime();
        this.checkTelegramStatus();
        setInterval(() => this.updateTime(), 1000);
    }
    
    async loadCSVData() {
        try {
            const response = await fetch('/api/csv-data');
            const result = await response.json();
            if (result.success && result.data) {
                this.csvData = result.data;
                console.log(`Loaded ${this.csvData.length} data points from CSV`);
            }
        } catch (error) {
            console.error('Error loading CSV data:', error);
        }
    }
    
    setupChart() {
        const ctx = document.getElementById('voltage-chart').getContext('2d');
        
        // Create gradient for the chart
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(0, 122, 255, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 122, 255, 0.0)');
        
        // Initialize with CSV data if available
        const initialData = this.csvData.length > 0 ? 
            this.csvData.slice(-50).map(d => d.voltage) : 
            Array(50).fill(220);
        
        const initialLabels = this.csvData.length > 0 ? 
            this.csvData.slice(-50).map(d => d.timestamp) : 
            Array(50).fill('');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: initialLabels,
                datasets: [{
                    label: 'Voltage',
                    data: initialData,
                    borderColor: '#007aff',
                    backgroundColor: gradient,
                    borderWidth: 4,
                    pointRadius: 0,
                    pointHoverRadius: 8,
                    pointHoverBackgroundColor: '#007aff',
                    pointHoverBorderColor: '#ffffff',
                    pointHoverBorderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 300,
                    easing: 'easeInOutQuart'
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                scales: {
                    x: {
                        display: false,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: false,
                        min: 180,
                        max: 300,
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                elements: {
                    point: {
                        hoverRadius: 10
                    }
                }
            }
        });
    }
    
    startMonitoring() {
        this.updateInterval = setInterval(async () => {
            await this.updateVoltage();
        }, 1000);
    }
    
    async updateVoltage() {
        try {
            // Get real data from CSV
            const response = await fetch('/api/voltage-data');
            const result = await response.json();
            
            if (result.success) {
                const voltage = result.voltage;
                const timestamp = result.timestamp;
                
                // Update voltage display
                this.currentVoltage.textContent = Math.round(voltage);
                
                // Update chart
                this.updateChart(voltage, timestamp);
                
                // Check for spikes
                if (voltage > 250) {
                    this.triggerSpike(voltage);
                } else {
                    this.resetSpike();
                }
                
                // Update last update time
                this.lastUpdate.textContent = 'Just now';
            }
        } catch (error) {
            console.error('Error updating voltage:', error);
            // Fallback to simulated data
            this.updateVoltageSimulated();
        }
    }
    
    updateVoltageSimulated() {
        // Fallback simulation if CSV data is not available
        const baseVoltage = 220;
        const fluctuation = (Math.random() - 0.5) * 20;
        const voltage = baseVoltage + fluctuation;
        
        this.currentVoltage.textContent = Math.round(voltage);
        this.updateChart(voltage, new Date().toLocaleTimeString());
        
        if (voltage > 250) {
            this.triggerSpike(voltage);
        } else {
            this.resetSpike();
        }
    }
    
    updateChart(voltage, timestamp) {
        if (!this.chart) return;
        
        // Add new data point
        this.chart.data.labels.push(timestamp);
        this.chart.data.datasets[0].data.push(voltage);
        
        // Remove old data points (keep last 50)
        if (this.chart.data.labels.length > 50) {
            this.chart.data.labels.shift();
            this.chart.data.datasets[0].data.shift();
        }
        
        // Update chart
        this.chart.update('none');
    }
    
    triggerSpike(spikeValue) {
        if (this.isSpikeActive) return;
        
        this.isSpikeActive = true;
        this.showSpikeAlert(spikeValue);
        this.sendTelegramAlert(spikeValue);
        
        // GSAP animations for spike effect
        gsap.to(this.currentVoltage, {
            scale: 1.2,
            duration: 0.2,
            yoyo: true,
            repeat: 3,
            ease: "power2.inOut"
        });
        
        gsap.to('#app-container', {
            backgroundColor: 'rgba(255, 69, 58, 0.1)',
            duration: 0.3,
            yoyo: true,
            repeat: 1,
            ease: "power2.inOut"
        });
        
        // Update status
        this.statusLight.classList.add('alert');
        this.statusText.textContent = 'ALERT';
    }
    
    resetSpike() {
        if (!this.isSpikeActive) return;
        
        this.isSpikeActive = false;
        this.statusLight.classList.remove('alert');
        this.statusText.textContent = 'System Online';
    }
    
    showSpikeAlert(spikeValue) {
        this.spikeAlert.classList.remove('hidden');
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            this.dismissAlert();
        }, 5000);
    }
    
    async sendTelegramAlert(spikeValue) {
        try {
            const response = await fetch('/api/telegram-alert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    voltage: spikeValue,
                    area: 'Istanbul, Kadıköy District',
                    severity: 'HIGH'
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showTelegramNotification();
            }
            
        } catch (error) {
            console.error('Error sending Telegram alert:', error);
        }
    }
    
    showTelegramNotification() {
        this.telegramNotification.classList.remove('hidden');
        
        setTimeout(() => {
            this.telegramNotification.classList.add('show');
        }, 100);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            this.telegramNotification.classList.remove('show');
            setTimeout(() => {
                this.telegramNotification.classList.add('hidden');
            }, 500);
        }, 3000);
    }
    
    async checkTelegramStatus() {
        try {
            const response = await fetch('/api/status');
            const result = await response.json();
            
            if (result.telegram_configured) {
                this.telegramStatus.textContent = 'Ready';
            } else {
                this.telegramStatus.textContent = 'Demo Mode';
            }
            
        } catch (error) {
            console.error('Error checking Telegram status:', error);
            this.telegramStatus.textContent = 'Demo Mode';
        }
    }
    
    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        this.lastUpdate.textContent = timeString;
    }
}

// Global function for alert dismissal
function dismissAlert() {
    if (window.voltageMonitor) {
        window.voltageMonitor.spikeAlert.classList.add('hidden');
        window.voltageMonitor.isSpikeActive = false;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.voltageMonitor = new VoltageMonitor();
});

// Add logo hover effects
document.addEventListener('DOMContentLoaded', () => {
    // Apply hover effects to Enerjisa logo
    const logos = document.querySelectorAll('.enerjisa-logo');
    
    logos.forEach(logo => {
        if (logo) {
            logo.addEventListener('mouseenter', () => {
                gsap.to(logo, {
                    scale: 1.1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
            
            logo.addEventListener('mouseleave', () => {
                gsap.to(logo, {
                    scale: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
        }
    });
});

// Create floating background particles
function createParticle() {
    const particle = document.createElement('div');
    particle.style.position = 'fixed';
    particle.style.width = '2px';
    particle.style.height = '2px';
    particle.style.background = 'rgba(0, 122, 255, 0.3)';
    particle.style.borderRadius = '50%';
    particle.style.pointerEvents = 'none';
    particle.style.zIndex = '1';
    
    // Random position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    
    document.body.appendChild(particle);
    
    // Animate particle
    gsap.to(particle, {
        y: -100,
        x: Math.random() * 50 - 25,
        opacity: 0,
        duration: Math.random() * 10 + 10,
        ease: "none",
        onComplete: () => {
            document.body.removeChild(particle);
        }
    });
}

// Create particles periodically
setInterval(createParticle, 2000); 