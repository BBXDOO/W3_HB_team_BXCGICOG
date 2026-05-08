from .base import FallbackAgent
from .bbex_core import BBEXCoreAgent
from .bbx19 import BBX19Agent
from .cast import CastAgent
from .chatgpt import ChatGPTAgent
from .copilot_gm import CopilotGmAgent
from .deepseek import DeepSeekAgent
from .gemini import GeminiAgent
from .grok import GrokAgent


AGENT_TABLE = {
    "ChatGPT": ChatGPTAgent,
    "Gemini": GeminiAgent,
    "Copilot-Gm": CopilotGmAgent,
    "DeepSeek": DeepSeekAgent,
    "Grok": GrokAgent,
    "Cast": CastAgent,
    "BBEX-Core": BBEXCoreAgent,
    "BBX19": BBX19Agent,
}


def get_agent(module_name):
    agent_cls = AGENT_TABLE.get(module_name, FallbackAgent)
    return agent_cls()
