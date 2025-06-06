import multiprocessing

# Worker configuration
workers = 2  # Start with fewer workers to reduce memory usage
worker_class = 'sync'  # Use sync workers instead of async for Django
threads = 2
worker_connections = 1000

# Timeout configuration
timeout = 120  # Increase timeout to 120 seconds
graceful_timeout = 60
keepalive = 5

# Memory optimization
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'ev_fleet_management'

# SSL configuration
forwarded_allow_ips = '*'
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
} 