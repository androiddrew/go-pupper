"""
Module contains all logic for retrieving CPU, Memory, and Disk stats.
"""
import psutil
import datetime as dt

from typing import Dict, Any
from .common import merge_into

STATIC_STATS = {"cpu_count": psutil.cpu_count(logical=True),
                "boot_time": dt.datetime.fromtimestamp(psutil.boot_time())}


def get_stats() -> Dict[str, Any]:
    """Main entrypoint for retrieving system stats."""
    load_avg = [round(x / psutil.cpu_count(logical=True) * 100, 2) for x in psutil.getloadavg()]
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    stats = {'load_avg': load_avg,
             'mem': {
                 'total': mem.total,
                 'used': mem.used,
                 'free': mem.free,
                 'shared': mem.shared if hasattr(mem, 'shared') else None,
                 'buffers': mem.buffers if hasattr(mem, 'buffers') else None,
                 'cached': mem.cached if hasattr(mem, 'cached') else None,
                 'available': mem.available,
                 'percent': mem.percent,
             },
             'tasks': get_tasks(),
             }
    stats.update(STATIC_STATS)
    return stats


def get_tasks() -> dict:
    """Retrieves a dictionary of task information."""
    tasks = {
        'total': 0,
        'running': 0,
        'sleeping': 0,
    }

    for p in psutil.process_iter():
        with p.oneshot():
            if p.status() == psutil.STATUS_RUNNING:
                tasks['running'] += 1
            if p.status() == psutil.STATUS_SLEEPING:
                tasks['sleeping'] += 1
            tasks['total'] += 1

    return tasks
