"""Structured live progress for the dashboard. Reporting only: nothing here changes results."""
import threading
import time

_LOCK = threading.Lock()
LIVE = {}


def reset():
    with _LOCK:
        LIVE.clear()
        LIVE.update({
            "target": None, "commit": None, "python": None, "model": None,
            "stage": None, "action": "Starting", "detail": "",
            "scan": {}, "baseline": {}, "deps": [], "forecast": {},
            "counters": {"environments": 0, "installs_ok": 0, "installs_failed": 0, "test_cases": 0,
                         "passed": 0, "failed": 0, "ai_calls": 0, "warnings": 0, "seconds": 0.0},
            "current_env": None, "events": [], "issues": [],
        })


reset()


def set(**kw):
    with _LOCK:
        LIVE.update(kw)


def event(kind, text, detail=""):
    with _LOCK:
        LIVE.setdefault("events", []).append({"t": time.time(), "kind": kind, "text": text, "detail": str(detail)[:1200]})
        del LIVE["events"][:-300]


def issue(severity, stage, title, detail=""):
    """severity: error | warning | info"""
    with _LOCK:
        LIVE.setdefault("issues", []).append({"t": time.time(), "severity": severity, "stage": stage,
                                              "title": title, "detail": str(detail)[:2000]})


def count(**kw):
    with _LOCK:
        c = LIVE.setdefault("counters", {})
        for k, v in kw.items():
            c[k] = round(c.get(k, 0) + v, 1)


def dep(name, **kw):
    with _LOCK:
        for d in LIVE.setdefault("deps", []):
            if d["name"] == name:
                d.update(kw)
                return
        LIVE["deps"].append({"name": name, **kw})


def snapshot():
    with _LOCK:
        import copy
        return copy.deepcopy(LIVE)
