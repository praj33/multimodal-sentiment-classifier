/**
 * 🚀 Advanced Analytics Dashboard JavaScript
 * Real-time sentiment analysis dashboard with WebSocket streaming
 */

class AdvancedAnalyticsDashboard {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.isPaused = false;
        this.feedItems = [];
        this.maxFeedItems = 50;
        
        // Chart instances
        this.charts = {
            sentimentTrend: null,
            sentimentDistribution: null,
            modality: null,
            geographic: null
        };
        
        // Data storage
        this.data = {
            summary: {},
            trends: [],
            geographic: [],
            realTimeFeed: []
        };
        
        this.init();
    }
    
    init() {
        this.setupWebSocket();
        this.setupEventListeners();
        this.initializeCharts();
        this.startPeriodicUpdates();
    }
    
    setupWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/analytics`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            this.isConnected = true;
            this.updateConnectionStatus('connected', 'Connected to real-time feed');
            console.log('WebSocket connected');
        };
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
        
        this.websocket.onclose = () => {
            this.isConnected = false;
            this.updateConnectionStatus('disconnected', 'Disconnected from feed');
            console.log('WebSocket disconnected');
            
            // Attempt to reconnect after 5 seconds
            setTimeout(() => {
                if (!this.isConnected) {
                    this.setupWebSocket();
                }
            }, 5000);
        };
        
        this.websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('disconnected', 'Connection error');
        };
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'initial_data':
                this.data.summary = data.summary;
                this.data.trends = data.trends;
                this.data.geographic = data.geographic;
                this.updateAllCharts();
                this.updateMetrics();
                break;
                
            case 'sentiment_update':
                if (!this.isPaused) {
                    this.addRealTimeFeedItem(data.data);
                    this.data.summary = data.summary;
                    this.updateMetrics();
                    this.updateRealTimeCharts();
                }
                break;
        }
    }
    
    updateConnectionStatus(status, message) {
        const statusElement = document.getElementById('connectionStatus');
        statusElement.className = `status-indicator ${status}`;
        
        let icon = '<div class="loading-spinner"></div>';
        if (status === 'connected') {
            icon = '<i class="fas fa-check-circle"></i>';
        } else if (status === 'disconnected') {
            icon = '<i class="fas fa-exclamation-triangle"></i>';
        }
        
        statusElement.innerHTML = `${icon}<span>${message}</span>`;
    }
    
    setupEventListeners() {
        // Period selection buttons
        document.querySelectorAll('.btn-chart[data-period]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.btn-chart[data-period]').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.updateTrendChart(e.target.dataset.period);
            });
        });
        
        // Feed controls
        document.getElementById('pauseFeed').addEventListener('click', () => {
            this.toggleFeedPause();
        });
        
        document.getElementById('clearFeed').addEventListener('click', () => {
            this.clearFeed();
        });
    }
    
    initializeCharts() {
        // Initialize Plotly charts
        this.initSentimentTrendChart();
        this.initSentimentDistributionChart();
        this.initModalityChart();
        this.initGeographicChart();
    }
    
    initSentimentTrendChart() {
        const layout = {
            title: '',
            xaxis: { title: 'Time' },
            yaxis: { title: 'Sentiment Count' },
            showlegend: true,
            margin: { t: 20, r: 20, b: 40, l: 40 },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)'
        };
        
        Plotly.newPlot('sentimentTrendChart', [], layout, {responsive: true});
    }
    
    initSentimentDistributionChart() {
        const layout = {
            title: '',
            showlegend: true,
            margin: { t: 20, r: 20, b: 20, l: 20 },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)'
        };
        
        Plotly.newPlot('sentimentDistributionChart', [], layout, {responsive: true});
    }
    
    initModalityChart() {
        const layout = {
            title: '',
            xaxis: { title: 'Modality' },
            yaxis: { title: 'Usage Count' },
            margin: { t: 20, r: 20, b: 40, l: 40 },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)'
        };
        
        Plotly.newPlot('modalityChart', [], layout, {responsive: true});
    }
    
    initGeographicChart() {
        const layout = {
            title: '',
            geo: {
                projection: { type: 'natural earth' },
                showland: true,
                landcolor: 'rgb(243, 243, 243)',
                coastlinecolor: 'rgb(204, 204, 204)'
            },
            margin: { t: 20, r: 20, b: 20, l: 20 }
        };
        
        Plotly.newPlot('geographicChart', [], layout, {responsive: true});
    }
    
    updateAllCharts() {
        this.updateTrendChart('24h');
        this.updateSentimentDistribution();
        this.updateModalityChart();
        this.updateGeographicChart();
    }
    
    updateTrendChart(period = '24h') {
        // Mock trend data for demonstration
        const hours = period === '1h' ? 1 : period === '6h' ? 6 : period === '24h' ? 24 : 168;
        const now = new Date();
        const timePoints = [];
        const positiveData = [];
        const negativeData = [];
        const neutralData = [];
        
        for (let i = hours; i >= 0; i--) {
            const time = new Date(now.getTime() - i * 60 * 60 * 1000);
            timePoints.push(time);
            positiveData.push(Math.floor(Math.random() * 20) + 10);
            negativeData.push(Math.floor(Math.random() * 15) + 5);
            neutralData.push(Math.floor(Math.random() * 10) + 5);
        }
        
        const traces = [
            {
                x: timePoints,
                y: positiveData,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Positive',
                line: { color: '#10b981', width: 3 },
                marker: { size: 6 }
            },
            {
                x: timePoints,
                y: negativeData,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Negative',
                line: { color: '#ef4444', width: 3 },
                marker: { size: 6 }
            },
            {
                x: timePoints,
                y: neutralData,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Neutral',
                line: { color: '#6b7280', width: 3 },
                marker: { size: 6 }
            }
        ];
        
        Plotly.redraw('sentimentTrendChart', traces);
    }
    
    updateSentimentDistribution() {
        const distribution = this.data.summary.sentiment_distribution || {};
        const values = Object.values(distribution);
        const labels = Object.keys(distribution);
        const colors = ['#10b981', '#ef4444', '#6b7280'];
        
        const trace = {
            values: values,
            labels: labels,
            type: 'pie',
            marker: { colors: colors },
            textinfo: 'label+percent',
            textposition: 'outside',
            hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        };
        
        Plotly.redraw('sentimentDistributionChart', [trace]);
    }
    
    updateModalityChart() {
        const modalities = this.data.summary.modality_distribution || {};
        const x = Object.keys(modalities);
        const y = Object.values(modalities);
        
        const trace = {
            x: x,
            y: y,
            type: 'bar',
            marker: {
                color: ['#2563eb', '#10b981', '#f59e0b'],
                opacity: 0.8
            },
            text: y,
            textposition: 'auto'
        };
        
        Plotly.redraw('modalityChart', [trace]);
    }
    
    updateGeographicChart() {
        // Mock geographic data
        const countries = ['USA', 'UK', 'Germany', 'France', 'Japan', 'Australia'];
        const values = countries.map(() => Math.floor(Math.random() * 100) + 10);
        
        const trace = {
            type: 'choropleth',
            locations: countries,
            z: values,
            locationmode: 'country names',
            colorscale: 'Viridis',
            colorbar: { title: 'Sentiment Count' }
        };
        
        Plotly.redraw('geographicChart', [trace]);
    }
    
    updateRealTimeCharts() {
        this.updateSentimentDistribution();
        this.updateModalityChart();
    }
    
    updateMetrics() {
        const summary = this.data.summary;
        
        // Update total predictions
        document.getElementById('totalPredictions').textContent = summary.total || 0;
        
        // Update average confidence
        const avgConf = ((summary.avg_confidence || 0) * 100).toFixed(1);
        document.getElementById('avgConfidence').textContent = `${avgConf}%`;
        
        // Update positive sentiment percentage
        const distribution = summary.sentiment_distribution || {};
        const total = Object.values(distribution).reduce((a, b) => a + b, 0);
        const positivePercent = total > 0 ? ((distribution.positive || 0) / total * 100).toFixed(1) : 0;
        document.getElementById('positiveSentiment').textContent = `${positivePercent}%`;
        
        // Update processing speed (mock data)
        document.getElementById('processingSpeed').textContent = `${Math.floor(Math.random() * 200) + 50}ms`;
    }
    
    addRealTimeFeedItem(data) {
        const feedElement = document.getElementById('realTimeFeed');
        
        // Create feed item
        const item = document.createElement('div');
        item.className = 'feed-item new';
        
        const sentimentClass = `sentiment-${data.sentiment}`;
        const timestamp = new Date(data.timestamp).toLocaleTimeString();
        
        item.innerHTML = `
            <div>
                <span class="sentiment-badge ${sentimentClass}">${data.sentiment}</span>
                <span class="ms-2">${data.modality}</span>
                <small class="text-muted ms-2">${timestamp}</small>
            </div>
            <div>
                <strong>${(data.confidence * 100).toFixed(1)}%</strong>
                <small class="text-muted ms-1">confidence</small>
            </div>
        `;
        
        // Add to top of feed
        feedElement.insertBefore(item, feedElement.firstChild);
        
        // Remove animation class after animation completes
        setTimeout(() => {
            item.classList.remove('new');
        }, 500);
        
        // Limit feed items
        this.feedItems.push(item);
        if (this.feedItems.length > this.maxFeedItems) {
            const oldItem = this.feedItems.shift();
            if (oldItem && oldItem.parentNode) {
                oldItem.parentNode.removeChild(oldItem);
            }
        }
    }
    
    toggleFeedPause() {
        this.isPaused = !this.isPaused;
        const btn = document.getElementById('pauseFeed');
        
        if (this.isPaused) {
            btn.innerHTML = '<i class="fas fa-play"></i> Resume';
            btn.classList.add('active');
        } else {
            btn.innerHTML = '<i class="fas fa-pause"></i> Pause';
            btn.classList.remove('active');
        }
    }
    
    clearFeed() {
        const feedElement = document.getElementById('realTimeFeed');
        feedElement.innerHTML = '';
        this.feedItems = [];
    }
    
    startPeriodicUpdates() {
        // Update charts every 30 seconds
        setInterval(() => {
            if (this.isConnected) {
                this.updateTrendChart();
            }
        }, 30000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AdvancedAnalyticsDashboard();
});
