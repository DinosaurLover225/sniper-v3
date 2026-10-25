import os, time, threading
import psutil
from pynput.keyboard import Controller, Key

_kb = Controller()
_HELD = ["w", "a", "s", "d", "e", "r", Key.space, Key.esc]


class FishSolBridge:
    def __init__(self, script_path, enabled=True):
        self.script_path = script_path      # full path to FishSol-v2.ahk
        self.enabled = enabled              # "pair with FishSol" setting

    def macro_running(self):
        for p in psutil.process_iter(["name", "cmdline"]):
            if (p.info["name"] or "").lower().startswith("autohotkey"):
                if any("fishsol" in (a or "").lower() for a in p.info["cmdline"] or []):
                    return True
        return False

    def ensure_launched(self):
        if not self.macro_running():
            os.startfile(self.script_path)  # uses your AHK v1 file association
            time.sleep(3)

    def pause(self):
        if not (self.enabled and self.macro_running()):
            return
        _kb.tap(Key.f2)
        time.sleep(1.5)                     # let the current loop notice toggle=false
        for k in _HELD:
            _kb.release(k)

    def resume(self):
        if not self.enabled:
            return
        self.ensure_launched()
        _kb.tap(Key.f1)


class SnipeSession:
    """join_fn is whatever main.py already uses to join a link."""
    def __init__(self, bridge, join_fn, press_join_fn, load_seconds=25):
        self.bridge, self.join, self.press_join = bridge, join_fn, press_join_fn
        self.load = load_seconds
        self._lock = threading.Lock()

    def run(self, snipe_link, hold_seconds, home_link):
        if not self._lock.acquire(blocking=False):
            return                          # already mid-snipe
        try:
            self.bridge.pause()
            self.join(snipe_link); self.press_join(); time.sleep(self.load)
            time.sleep(hold_seconds)        # stay in the biome
            if home_link:
                self.join(home_link); self.press_join(); time.sleep(self.load)
            self.bridge.resume()
        finally:
            self._lock.release()
