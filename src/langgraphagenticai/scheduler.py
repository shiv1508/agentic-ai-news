from importlib import import_module
import os
import logging
from typing import Callable, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)
_scheduler: Optional[BackgroundScheduler] = None

def _load_callable(path: str) -> Callable:
    """
    Load a callable by path "module.sub:callable_name".
    """
    if ":" not in path:
        raise ValueError("SCHEDULE_JOB_FUNC must be in format 'module:callable'")
    module_path, func_name = path.split(":", 1)
    module = import_module(module_path)
    func = getattr(module, func_name)
    if not callable(func):
        raise ValueError(f"{path} is not callable")
    return func

def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    job_func_path = os.getenv("SCHEDULE_JOB_FUNC")
    if not job_func_path:
        logger.info("No SCHEDULE_JOB_FUNC set; scheduler will not start.")
        return None

    try:
        func = _load_callable(job_func_path)
    except Exception as e:
        logger.exception("Failed to load scheduled callable: %s", e)
        return None

    trigger_type = os.getenv("SCHEDULE_JOB_TRIGGER", "interval").lower()

    scheduler = BackgroundScheduler()
    if trigger_type == "interval":
        seconds = int(os.getenv("SCHEDULE_JOB_SECONDS", "3600"))
        trigger = IntervalTrigger(seconds=seconds)
    elif trigger_type == "cron":
        # Expect SCHEDULE_JOB_CRON to be a space-separated cron string "min hour day month dow"
        cron_expr = os.getenv("SCHEDULE_JOB_CRON", "")
        if not cron_expr:
            raise ValueError("SCHEDULE_JOB_CRON required when SCHEDULE_JOB_TRIGGER=cron")
        parts = cron_expr.split()
        # Map up to five parts (minute hour day month day_of_week)
        cron_kwargs = {}
        if len(parts) >= 1: cron_kwargs["minute"] = parts[0]
        if len(parts) >= 2: cron_kwargs["hour"] = parts[1]
        if len(parts) >= 3: cron_kwargs["day"] = parts[2]
        if len(parts) >= 4: cron_kwargs["month"] = parts[3]
        if len(parts) >= 5: cron_kwargs["day_of_week"] = parts[4]
        trigger = CronTrigger(**cron_kwargs)
    else:
        raise ValueError(f"Unsupported SCHEDULE_JOB_TRIGGER: {trigger_type}")

    scheduler.add_job(func, trigger, id="agentic_ai_news_summary", replace_existing=True)
    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler started with job %s using trigger %s", job_func_path, trigger_type)
    return scheduler

def shutdown_scheduler():
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Scheduler shut down.")