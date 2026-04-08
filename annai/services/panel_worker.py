# annai/services/panel_worker.py

import asyncio
import random


class PanelWorker:
    def __init__(self, panel_name: str, logger=None):
        self.panel_name = panel_name
        self.logger = logger

    def _log(self, msg: str):
        if self.logger:
            self.logger.info(f"[{self.panel_name}] {msg}")

    async def step1_init_trigger(self):
        self._log("Step 1 started")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        return f"{self.panel_name}-data-1"

    async def step2_init_stage(self, data):
        self._log(f"Step 2 with {data}")
        await asyncio.sleep(random.uniform(1.0, 2.0))
        return f"{data}->processed"

    async def step3_end_trigger(self, data):
        self._log(f"Step 3 with {data}")
        await asyncio.sleep(random.uniform(0.5, 1.0))
        return f"{data}->final"

    async def finalize(self, data):
        self._log(f"Finalizing {data}")
        await asyncio.sleep(0.3)