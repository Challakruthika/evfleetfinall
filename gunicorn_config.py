import multiprocessing
import os
import resource

# Worker configuration - absolute minimum
workers = 1  # Use only one worker to minimize memory usage
worker_class = 'custom_worker.MemoryEfficientWorker'  # Use custom worker
threads = 1  # Minimize thread count
worker_connections = 50  # Reduce connections

# Timeout configuration
timeout = 20  # Reduce timeout to fail fast
graceful_timeout = 20
keepalive = 2

# Memory optimization
max_requests = 50  # Reduce max requests before worker restart
max_requests_jitter = 5
limit_request_line = 1024
limit_request_fields = 50
limit_request_field_size = 1024

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'  # Increase log level for debugging
capture_output = True
enable_stdio_inheritance = True

# Process naming
proc_name = 'ev_fleet_management'

# SSL configuration
forwarded_allow_ips = '*'
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Preload app to save memory
preload_app = True

def when_ready(server):
    """Called just after the server is started."""
    try:
        # Set process memory limit (512MB)
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, -1))
        
        # Set open files limit
        resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
        
        # Disable core dumps
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, ValueError):
        pass 