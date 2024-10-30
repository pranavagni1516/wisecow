import psutil
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="system_health.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Thresholds
CPU_THRESHOLD = 80  # in percentage
MEMORY_THRESHOLD = 80  # in percentage
DISK_THRESHOLD = 80  # in percentage
PROCESS_THRESHOLD = 200  # example threshold for number of processes

def log_message(message):
    """Logs message to console and log file."""
    print(message)
    logging.info(message)

def check_cpu_usage():
    """Check CPU usage and log alert if it exceeds threshold."""
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        log_message(f"ALERT: High CPU usage detected! Current usage: {cpu_usage}%")
    else:
        log_message(f"CPU usage is normal: {cpu_usage}%")

def check_memory_usage():
    """Check memory usage and log alert if it exceeds threshold."""
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        log_message(f"ALERT: High Memory usage detected! Current usage: {memory_usage}%")
    else:
        log_message(f"Memory usage is normal: {memory_usage}%")

def check_disk_usage():
    """Check disk space usage and log alert if it exceeds threshold."""
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    if disk_usage > DISK_THRESHOLD:
        log_message(f"ALERT: High Disk usage detected! Current usage: {disk_usage}%")
    else:
        log_message(f"Disk usage is normal: {disk_usage}%")

def check_running_processes():
    """Check number of running processes and log alert if it exceeds threshold."""
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        log_message(f"ALERT: High number of running processes detected! Current count: {process_count}")
    else:
        log_message(f"Number of running processes is normal: {process_count}")

def main():
    """Main function to check all metrics."""
    log_message("Starting system health check")
    check_cpu_usage()
    check_memory_usage()
    check_disk_usage()
    check_running_processes()
    log_message("System health check complete\n")

if __name__ == "__main__":
    main()
