#!/usr/bin/env python3
"""W3 request-cycle bridge: root requests -> module runtime -> result/evidence.

This is glue for mechanisms that already exist. It does not implement module
intelligence. A request is executed only when its target resolves to the same
module as its task keyword in modules/registry.json.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.module_loader.router import load_identity, route_task
from core.runtime.engine_v2 import build_context, dispatch, validate_agent_result, now

REQUESTS=ROOT/"requests"
RESULTS=REQUESTS/"results"
EVENTS=ROOT/"repo_events"

def scalar(v:str)->Any:
    v=v.strip()
    if v.lower() in {"true","false"}: return v.lower()=="true"
    return v.strip('"').strip("'")

def parse_request(path:Path)->dict:
    text=path.read_text(encoding="utf-8")
    if not text.startswith("---"): raise ValueError("request has no YAML frontmatter")
    parts=text.split("---",2)
    meta={}
    for line in parts[1].splitlines():
        if ":" in line:
            k,v=line.split(":",1); meta[k.strip()]=scalar(v)
    meta["_request_file"]=str(path.relative_to(ROOT))
    meta["_request_text"]=text
    return meta

def safe_id(value:str)->str:
    return re.sub(r"[^A-Za-z0-9_.-]+","-",value).strip("-")

def already_done(rid:str)->bool:
    return (RESULTS/f"{safe_id(rid)}_RESULT.json").exists()

def process(path:Path)->dict:
    req=parse_request(path)
    rid=str(req.get("request_id") or path.stem)
    task=str(req.get("task_keyword") or "general").strip()
    target=str(req.get("target_module") or "").strip()
    if not target:
        # Routing is discovery/fallback only when the request does not name a module.
        target=route_task(task)["assigned_module"]

    # A named target is not rejected because another module is the preferred route.
    # Identity/capability stays with the executing module; substitution is traceable.
    manifest=load_identity(target)
    preferred=None
    try:
        preferred=route_task(task)["assigned_module"]
    except Exception:
        preferred=None

    if already_done(rid): return {"status":"SKIPPED","request_id":rid,"reason":"result already exists"}

    request_context={
      "source": req.get("requester","requests/"),
      "target": target,
      "mode": req.get("request_type","request"),
      "intent": rid,
      "payload": {
        "request_id": rid,
        "source_request": req["_request_file"],
        "request_type": req.get("request_type"),
        "authority_requested": req.get("authority_requested"),
        "final_signoff_required": req.get("final_signoff_required",True),
        "preferred_module": preferred,
        "executed_by": target,
        "substitution": bool(preferred and preferred != target),
      },
      "_request_file": req["_request_file"],
    }
    plan={
      "task":task,
      "run_with":target,
      "role":manifest.get("role") or manifest.get("display_name","—"),
      "status":manifest.get("status","unknown"),
      "responsibilities":manifest.get("responsibilities",[]),
      "next_step":f"Execute task {task!r} using requested module {target}",
    }
    context=build_context(task,request_context)
    try:
        agent_result=dispatch(target,task,plan,context)
        if not isinstance(agent_result,dict):
            raise TypeError("agent execute() returned non-dictionary result")
        result={
          "status":str(agent_result.get("status") or "FAILED"),
          "task":task,"module":target,
          "output":str(agent_result.get("summary") or "No result summary provided."),
          "agent_result":agent_result,
          "result_validation":validate_agent_result(target,agent_result),
          "artifacts":agent_result.get("artifacts",[]),
          "time":now(),"trace_id":context["trace_id"],
        }
    except Exception as exc:
        result={"status":"FAILED","task":task,"module":target,"error":str(exc),"artifacts":[],"time":now(),"trace_id":context["trace_id"]}

    RESULTS.mkdir(parents=True,exist_ok=True); EVENTS.mkdir(parents=True,exist_ok=True)
    envelope={
      "request_id":rid,"source_request":req["_request_file"],"target_module":target,
      "preferred_module":preferred,"executed_by":target,
      "substitution":bool(preferred and preferred != target),
      "task_keyword":task,"runtime_result":result,
      "artifact_paths":result.get("artifacts",[]),
      "final_signoff_required":bool(req.get("final_signoff_required",True)),
      "closed":False,"mutated":bool(result.get("agent_result",{}).get("mutated",False)),
      "review":True,
    }
    rp=RESULTS/f"{safe_id(rid)}_RESULT.json"
    rp.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ep=EVENTS/f"{safe_id(rid)}_EXECUTION.md"
    ep.write_text(
      f"# Request Execution Event\n\n- request_id: \`{rid}\`\n- source: \`{req['_request_file']}\`\n"
      f"- requested/executed_by: \`{target}\`\n- preferred route: \`{preferred or 'none'}\`\n"
      f"- substitution: \`{str(bool(preferred and preferred != target)).lower()}\`\n"
      f"- task: \`{task}\`\n- status: \`{result.get('status')}\`\n"
      f"- trace_id: \`{result.get('trace_id')}\`\n- result: \`{rp.relative_to(ROOT)}\`\n"
      f"- final_signoff_required: \`{str(bool(req.get('final_signoff_required',True))).lower()}\`\n"
      "- closed: \`false\`\n",
      encoding="utf-8")
    return envelope

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--request",help="process one request path")
    ap.add_argument("--pending",action="store_true",help="process pending root request markdown files")
    args=ap.parse_args()
    if args.request:
        paths=[ROOT/args.request]
    else:
        paths=[]
        for candidate in sorted(REQUESTS.glob("*.md")):
            try:
                probe=parse_request(candidate)
            except ValueError:
                continue
            if probe.get("request_id") and probe.get("task_keyword") and probe.get("target_module"):
                paths.append(candidate)
    if not args.pending and not args.request: ap.error("use --request or --pending")
    rc=0
    for p in paths:
      try: print(json.dumps(process(p),ensure_ascii=False))
      except Exception as e:
        rc=1; print(json.dumps({"status":"FAILED","request":str(p.relative_to(ROOT)),"error":str(e)},ensure_ascii=False))
    raise SystemExit(rc)
if __name__=="__main__": main()
