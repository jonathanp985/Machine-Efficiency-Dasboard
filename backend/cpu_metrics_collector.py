import psutil
import time
from datetime import datetime

def collect_metrics():
    # Grab CPU frequency info
    freq = psutil.cpu_freq()
    freq_percent = (freq.current / freq.max) * 100 if freq and freq.max else None

    # CPU temperature
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current
        elif 'cpu-thermal' in temps:  # for some ARM devices
            cpu_temp = temps['cpu-thermal'][0].current
        else:
            cpu_temp = 55
    except:
        cpu_temp = 55

    # Collect all metrics in a dictionary
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "cpu_freq": freq.current if freq else None,
        "cpu_freq_percent": freq_percent,
        "cpu_idle_time": psutil.cpu_times_percent().idle,
        "cpu_temperature": cpu_temp,
        "num_cores": psutil.cpu_count(logical=False),
        "num_threads": psutil.cpu_count(logical=True),
        "load_avg_1m": psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else None,
        "uptime": time.time() - psutil.boot_time(),
        "memory_usage": psutil.virtual_memory().percent,
        "swap_usage": psutil.swap_memory().percent,
        "disk_read_bytes": psutil.disk_io_counters().read_bytes,
        "disk_write_bytes": psutil.disk_io_counters().write_bytes,
        "network_sent_bytes": psutil.net_io_counters().bytes_sent,
        "network_recv_bytes": psutil.net_io_counters().bytes_recv,
        "context_switches": psutil.cpu_stats().ctx_switches,
        "interrupts": psutil.cpu_stats().interrupts,
        "cpu_percent_per_core": sum(psutil.cpu_percent(percpu=True)) / psutil.cpu_count(logical=True)
    }


def calculate_score(metrics):
    score = 100

    # CPU usage
    if metrics['cpu_usage'] > 90:
        score -= 30
    elif metrics['cpu_usage'] > 70:
        score -= 20
    elif metrics['cpu_usage'] > 50:
        score -= 10

    # CPU frequency percent
    if metrics['cpu_freq_percent'] is not None and metrics['cpu_freq_percent'] < 40:
        score -= 10

    # CPU idle time
    if metrics['cpu_idle_time'] < 10:
        score -= 15
    elif metrics['cpu_idle_time'] < 30:
        score -= 5

    # CPU temperature
    if metrics['cpu_temperature'] is not None:
        if metrics['cpu_temperature'] > 85:
            score -= 25
        elif metrics['cpu_temperature'] > 70:
            score -= 15
        elif metrics['cpu_temperature'] > 60:
            score -= 5

    # Number of cores/threads — low core count = lower ceiling
    if metrics['num_cores'] <= 2:
        score -= 5
    if metrics['num_threads'] <= 4:
        score -= 5

    # Load average (1m)
    if metrics['load_avg_1m'] is not None:
        load_per_core = metrics['load_avg_1m'] / (metrics['num_threads'] or 1)
        if load_per_core > 1.5:
            score -= 15
        elif load_per_core > 1.0:
            score -= 10
        elif load_per_core > 0.7:
            score -= 5

    # Uptime — longer uptime is slightly better (e.g., stable system)
    if metrics['uptime'] < 600:  # less than 10 mins
        score -= 5
    elif metrics['uptime'] > 86400:  # more than 1 day
        score += 5

    # Memory usage
    if metrics['memory_usage'] > 90:
        score -= 15
    elif metrics['memory_usage'] > 75:
        score -= 10
    elif metrics['memory_usage'] > 60:
        score -= 5

    # Swap usage
    if metrics['swap_usage'] > 50:
        score -= 10
    elif metrics['swap_usage'] > 20:
        score -= 5

    # Disk I/O
    if metrics['disk_read_bytes'] + metrics['disk_write_bytes'] > 10**9:
        score -= 5

    # Network I/O
    if metrics['network_sent_bytes'] + metrics['network_recv_bytes'] > 10**9:
        score -= 5

    # Context switches — high = heavy multitasking
    if metrics['context_switches'] > 100000:
        score -= 5

    # Interrupts
    if metrics['interrupts'] > 50000:
        score -= 5

    # Per-core average usage
    if metrics['cpu_percent_per_core'] > 90:
        score -= 20
    elif metrics['cpu_percent_per_core'] > 70:
        score -= 10
    elif metrics['cpu_percent_per_core'] > 50:
        score -= 5

    # Running applications (if using this)
    if 'num_running_apps' in metrics:
        if metrics['num_running_apps'] > 30:
            score -= 10
        elif metrics['num_running_apps'] > 20:
            score -= 5

    # Clamp score to 0–100
    return max(0, min(100, round(score)))