'''
Memory Usage Monitoring
'''
import psutil

psutil.virtual_memory().percent

dict(psutil.virtual_memory()._asdict())
