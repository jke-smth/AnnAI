import asyncio
import random
import os
from typing import Dict, Optional

from PySide6.QtCore import QThread, Signal

from annai.services.panel_state_machine import PanelState
from annai.services.text_engine import TextEngine


# panel states:
# - idle
# - init_trigger: this is where we take the initial prompt and instructions, and do any initial processing needed to prepare for the main work in the next stages. This is also the stage where we would pull in any additional context if needed (e.g. past responses, external knowledge, etc.)
# - init_stage: this is where we do any additional processing needed before the main trigger, such as calling external APIs, doing computations, etc. The output of this stage would be used as input for the end_trigger stage.
# - end_trigger: this is where the main "work" happens, prompt and instructions being sent, response being generated, etc. This is the stage that would typically take the longest time, and where we would want to show the "working" state in the UI.
# - end_stage: this is where the "response" is received and processed, and any finalization happens (e.g. sending response to other panels, TTS, etc.)
# - stopped

class PanelWorker:
    def __init__(self, panel_name: str, logger=None):
        self.panel_name = panel_name
        self.logger = logger
        self._results: Dict[PanelState, str] = {}
        self._initial_input: Optional[Dict[str, str]] = None
        self.text_engine = TextEngine(model = os.getenv("ANNAI_OLLAMA_MODEL", "qwen3:4b"), base_url = os.getenv("ANNAI_OLLAMA_URL", "http://127.0.0.1:11434"), logger=logger)

    def _log(self, msg: str):
        if self.logger:
            self.logger.info(f"[{self.panel_name}] {msg}")

    def reset(self):
        self._results.clear()
        self._initial_input = None

    def get_result(self, state: PanelState):
        return self._results.get(state)

    def set_initial_input(self, prompt: str, instructions: str):
        self._initial_input = {
            "prompt": prompt.strip(),
            "instructions": instructions.strip(),
        }

    async def step1_init_trigger(self, prompt: str, instructions: str):
        self._log("Step 1 started")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        return (
            f"{self.panel_name}-data-1 | "
            f"instructions={instructions or '<empty>'} | "
            f"prompt={prompt or '<empty>'}"
        )
    
    async def step2_init_stage(self, data1):
        self._log(f"Step 2 started with data: {data1}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        initial_input = self._require_initial_input()
        return self._build_generation_prompt(
            prompt=initial_input["prompt"],
            instructions=initial_input["instructions"],
            prepared_context=data1,
        )
    
    async def step3_end_trigger(self, data2):
        self._log(f"Step 3 started with data: {data2}")
        system_prompt = self._build_system_prompt()
        return await self.text_engine.generate(prompt=data2, system=system_prompt)
    
    async def step4_end_stage(self, data3):
        self._log(f"Step 4 started with data: {data3}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        return f"{self.panel_name}-final-result-based-on-{data3}"

    async def run_for_state(self, state: PanelState):
        if state == PanelState.INIT_TRIGGER:
            initial_input = self._require_initial_input()
            result = await self.step1_init_trigger(
                initial_input["prompt"],
                initial_input["instructions"],
            )
        elif state == PanelState.INIT_STAGE:
            result = await self.step2_init_stage(self._require_result(PanelState.INIT_TRIGGER))
        elif state == PanelState.END_TRIGGER:
            result = await self.step3_end_trigger(self._require_result(PanelState.INIT_STAGE))
        elif state == PanelState.END_STAGE:
            result = await self.step4_end_stage(self._require_result(PanelState.END_TRIGGER))
        else:
            raise ValueError(f"No worker step defined for state '{state.value}'")

        self._results[state] = result
        self._log(f"Completed {state.value}: {result}")
        return result

    def _require_result(self, state: PanelState):
        if state not in self._results:
            raise RuntimeError(
                f"Missing prerequisite result for '{state.value}'. "
                "Run the previous panel step first."
            )
        return self._results[state]

    def _require_initial_input(self):
        if self._initial_input is None:
            raise RuntimeError("Missing initial panel input. Add prompt/instructions before stepping.")
        return self._initial_input

    def _build_generation_prompt(self, prompt: str, instructions: str, prepared_context: str) -> str:
        instructions_text = instructions or "No extra instructions provided."
        prompt_text = prompt or "No prompt provided."
        return (
            f"Panel: {self.panel_name}\n"
            f"Prepared context:\n{prepared_context}\n\n"
            f"Instructions:\n{instructions_text}\n\n"
            f"Prompt:\n{prompt_text}"
        )

    def _build_system_prompt(self) -> str:
        return (
            "You are the text engine for the AnnAI panel workflow. "
            "Follow the provided instructions carefully and answer the prompt directly."
        )


class PanelStepThread(QThread):
    step_started = Signal(str)
    step_finished = Signal(str)
    step_failed = Signal(str)

    def __init__(self, worker: PanelWorker, state: PanelState):
        super().__init__()
        self.worker = worker
        self.state = state

    def run(self):
        self.step_started.emit(self.state.value)
        try:
            result = asyncio.run(self.worker.run_for_state(self.state))
        except Exception as exc:
            self.step_failed.emit(str(exc))
            return

        self.step_finished.emit(result)
