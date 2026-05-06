"""
W3 LLM Adapter — MVP Integration Layer
Path: core/adapters/llm_adapter.py

Purpose:
- Connect W3 module system to real LLM APIs (GPT, Gemini)
- Write results to module output paths declared in module.json
- Single integration point; no large framework needed

Requires:
  pip install openai google-generativeai

Environment variables:
  OPENAI_API_KEY    — your OpenAI API key
  GEMINI_API_KEY    — your Google Gemini API key

Author: BBX19 / W3
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path


# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Output directory per module (relative to repo root)
# Keys match engine_v2 dispatch table
MODULE_OUTPUT_PATHS = {
    "ChatGPT":   "ChatGPT/modules/ChatGPT/reports",
    "Gemini":    "Gemini/modules/Gemini/reports",
    "Grok":      "Grok/modules/Grok/reports",
    "DeepSeek":  "DeepSeek/modules/DeepSeek/reports",
    "Copilot-Gm": "Copilot-Gm/reports",
    "Cast":      "Cast/reports",
    "BBEX-Core": "BBEX-Core/public/reports",
    "BBX19":     "BBX19/status",
}

# Default models
DEFAULT_GPT_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"

# Modules routed to GPT by default
GPT_MODULES = {"ChatGPT", "BBX19", "Cast", "Copilot-Gm"}

# Modules routed to Gemini by default
GEMINI_MODULES = {"Gemini", "DeepSeek", "Grok", "BBEX-Core"}


class LLMAdapterError(Exception):
    pass


# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------

def _now_str():
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")


def _date_str():
    return datetime.utcnow().strftime("%Y-%m-%d")


def _output_dir(module_name):
    """Return (and create if needed) the output directory for a module."""
    rel_path = MODULE_OUTPUT_PATHS.get(module_name)
    if not rel_path:
        raise LLMAdapterError(f"No output path configured for module: {module_name}")
    path = REPO_ROOT / rel_path
    path.mkdir(parents=True, exist_ok=True)
    return path


def _safe_filename(task):
    """Convert a task string to a safe filename fragment."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in task)[:60]


def _write_result(module_name, task, content):
    """Write LLM output to the module's output folder as a Markdown file."""
    out_dir = _output_dir(module_name)
    filename = f"{_date_str()}_{_safe_filename(task)}.md"
    filepath = out_dir / filename

    header = (
        f"# W3 Output — {module_name}\n\n"
        f"**Task:** {task}  \n"
        f"**Module:** {module_name}  \n"
        f"**Generated:** {_now_str()}  \n\n"
        f"---\n\n"
    )

    filepath.write_text(header + content, encoding="utf-8")
    return str(filepath.relative_to(REPO_ROOT))


# -------------------------------------------------------
# GPT ADAPTER
# -------------------------------------------------------

def call_gpt(task, model=DEFAULT_GPT_MODEL, system_prompt=None):
    """
    Call OpenAI ChatCompletion API.

    Requires:
        pip install openai
        OPENAI_API_KEY env var

    Returns:
        str — model response text
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise LLMAdapterError(
            "openai package not installed. Run: pip install openai"
        ) from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise LLMAdapterError(
            "OPENAI_API_KEY environment variable not set."
        )

    client = OpenAI(api_key=api_key)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": task})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content


# -------------------------------------------------------
# GEMINI ADAPTER
# -------------------------------------------------------

def call_gemini(task, model=DEFAULT_GEMINI_MODEL, system_prompt=None):
    """
    Call Google Gemini GenerativeAI API.

    Requires:
        pip install google-generativeai
        GEMINI_API_KEY env var

    Returns:
        str — model response text
    """
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise LLMAdapterError(
            "google-generativeai package not installed. "
            "Run: pip install google-generativeai"
        ) from exc

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise LLMAdapterError(
            "GEMINI_API_KEY environment variable not set."
        )

    genai.configure(api_key=api_key)
    gen_model = genai.GenerativeModel(model)

    prompt = task
    if system_prompt:
        prompt = f"{system_prompt}\n\n{task}"

    response = gen_model.generate_content(prompt)
    return response.text


# -------------------------------------------------------
# UNIFIED DISPATCH
# -------------------------------------------------------

def _pick_backend(module_name):
    """Return 'gpt' or 'gemini' based on module name."""
    if module_name in GPT_MODULES:
        return "gpt"
    if module_name in GEMINI_MODULES:
        return "gemini"
    # default fallback
    return "gpt"


def run_module(module_name, task, backend=None, model=None, system_prompt=None):
    """
    Run a W3 module task using the real LLM API and write output to the
    module's output folder.

    Args:
        module_name (str): One of the 8 W3 modules.
        task (str): Natural language task description.
        backend (str|None): "gpt" or "gemini". Auto-detected if None.
        model (str|None): Override the default model.
        system_prompt (str|None): Optional system/context prompt.

    Returns:
        dict: {status, module, task, output_file, content_preview, time}

    Example:
        result = run_module("ChatGPT", "design a REST API for W3 module registry")
        print(result["output_file"])
    """
    started = time.time()

    if module_name not in MODULE_OUTPUT_PATHS:
        raise LLMAdapterError(
            f"Unknown module: {module_name}. "
            f"Valid modules: {list(MODULE_OUTPUT_PATHS.keys())}"
        )

    backend = backend or _pick_backend(module_name)

    try:
        if backend == "gpt":
            content = call_gpt(task, model=model or DEFAULT_GPT_MODEL, system_prompt=system_prompt)
        elif backend == "gemini":
            content = call_gemini(task, model=model or DEFAULT_GEMINI_MODEL, system_prompt=system_prompt)
        else:
            raise LLMAdapterError(f"Unknown backend: {backend}. Use 'gpt' or 'gemini'.")

        output_file = _write_result(module_name, task, content)

        return {
            "status": "SUCCESS",
            "module": module_name,
            "backend": backend,
            "task": task,
            "output_file": output_file,
            "content_preview": content[:200] + ("..." if len(content) > 200 else ""),
            "latency_ms": int((time.time() - started) * 1000),
            "time": _now_str(),
        }

    except Exception as exc:
        return {
            "status": "FAILED",
            "module": module_name,
            "backend": backend,
            "task": task,
            "error": str(exc),
            "time": _now_str(),
        }


# -------------------------------------------------------
# CLI ENTRY POINT
# -------------------------------------------------------

def _cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="W3 LLM Adapter — run a module task using GPT or Gemini"
    )
    parser.add_argument(
        "--module", "-m",
        required=True,
        choices=list(MODULE_OUTPUT_PATHS.keys()),
        help="W3 module name (e.g. ChatGPT, Gemini, Grok)",
    )
    parser.add_argument(
        "--task", "-t",
        required=True,
        help='Task description (e.g. "design architecture for W3 v0.3")',
    )
    parser.add_argument(
        "--backend", "-b",
        choices=["gpt", "gemini"],
        default=None,
        help="LLM backend to use (auto-detected from module if omitted)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"Model override (default GPT: {DEFAULT_GPT_MODEL}, Gemini: {DEFAULT_GEMINI_MODEL})",
    )
    parser.add_argument(
        "--system-prompt", "-s",
        default=None,
        help="Optional system/context prompt",
    )

    args = parser.parse_args()

    result = run_module(
        module_name=args.module,
        task=args.task,
        backend=args.backend,
        model=args.model,
        system_prompt=args.system_prompt,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] == "SUCCESS":
        print(f"\n✅ Output written to: {result['output_file']}")
    else:
        print(f"\n❌ Failed: {result.get('error')}")


if __name__ == "__main__":
    _cli()
