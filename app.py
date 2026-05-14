"""
Flask Application for Service Selector Dashboard
Deployable to OpenShift Container Platform (OCP)
"""

from flask import Flask, render_template, send_from_directory, jsonify
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='.',
            template_folder='.')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Health check endpoint for OCP
@app.route('/health')
def health():
    """Health check endpoint for OpenShift readiness/liveness probes"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'service-selector-dashboard'
    }), 200

# Readiness probe
@app.route('/ready')
def ready():
    """Readiness probe for OpenShift"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Main dashboard route
@app.route('/')
def index():
    """Serve the main service selector dashboard"""
    try:
        return render_template('service_selector.html')
    except Exception as e:
        logger.error(f"Error serving dashboard: {str(e)}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

# Serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('.', filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

# API endpoint for chart data (if needed)
@app.route('/api/chart-data')
def get_chart_data():
    """API endpoint to serve chart data"""
    try:
        # Check if chart_data.js exists
        if os.path.exists('chart_data.js'):
            with open('chart_data.js', 'r') as f:
                data = f.read()
            return data, 200, {'Content-Type': 'application/javascript'}
        else:
            return jsonify({'error': 'Chart data not found'}), 404
    except Exception as e:
        logger.error(f"Error loading chart data: {str(e)}")
        return jsonify({'error': 'Failed to load chart data'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# Application info endpoint
@app.route('/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'name': 'Service Selector Dashboard',
        'version': '1.0.0',
        'description': 'Interactive dashboard for service configuration and analysis',
        'endpoints': {
            '/': 'Main dashboard',
            '/health': 'Health check',
            '/ready': 'Readiness probe',
            '/info': 'Application information',
            '/api/chart-data': 'Chart data API'
        }
    })

if __name__ == '__main__':
    # Get port from environment variable (OCP will set this)
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Service Selector Dashboard on {host}:{port}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )

# Made with Bob
