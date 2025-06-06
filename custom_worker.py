import os
import gc
import psutil
import resource
from gunicorn.workers.sync import SyncWorker

class MemoryEfficientWorker(SyncWorker):
    def handle_request(self, *args, **kwargs):
        # Force garbage collection before each request
        gc.collect()
        
        # Get the current process
        process = psutil.Process(os.getpid())
        
        # Set memory limit to 450MB (leaving some headroom)
        memory_limit = 450 * 1024 * 1024  # 450MB in bytes
        
        try:
            # Set process memory limit
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # Handle the request
            result = super().handle_request(*args, **kwargs)
            
            # Force garbage collection after request
            gc.collect()
            
            return result
            
        except MemoryError:
            # If we hit memory limit, force garbage collection and try again
            gc.collect()
            return super().handle_request(*args, **kwargs)
        finally:
            # Always run garbage collection at the end
            gc.collect()
    
    def handle(self, *args, **kwargs):
        # Set lower soft and hard limits for number of open files
        resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
        
        # Disable core dumps
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        
        # Set CPU time limit (30 seconds)
        resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
        
        return super().handle(*args, **kwargs) 