from .base import FallbackAgent
from .bbex_core import BBEXCoreAgent
from .bbx19 import BBX19Agent
from .cast import CastAgent
from .chatgpt import ChatGPTAgent
from .copilot_gm import CopilotGmAgent
from .deepseek import DeepSeekAgent
from .dtml import DTMLAgent
from .gemini import GeminiAgent
from .grok import GrokAgent
from .lrc2 import LRC2Agent
from .psp2 import PSP2Agent
from .redr import REDRAgent


AGENT_TABLE = {
    "ChatGPT": ChatGPTAgent,
    "Gemini": GeminiAgent,
    "Copilot-Gm": CopilotGmAgent,
    "DeepSeek": DeepSeekAgent,
    "Grok": GrokAgent,
    "Cast": CastAgent,
    "BBEX-Core": BBEXCoreAgent,
    "BBX19": BBX19Agent,
    "PSP2": PSP2Agent,
    "REDR": REDRAgent,
    "DTML": DTMLAgent,
    "LRC2": LRC2Agent,
}


def get_agent(module_name):
    agent_cls = AGENT_TABLE.get(module_name, FallbackAgent)
    return agent_cls()
