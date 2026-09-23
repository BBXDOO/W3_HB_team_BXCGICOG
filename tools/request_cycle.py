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
from core.module_loader.router import load_identity, load_registry, route_task
from core.runtime.engine_v2 import build_context, dispatch, validate_agent_result, now
from core.memory.memory_bus import add_memory

REQUESTS=ROOT/"requests"
RESULTS=REQUESTS/"results"
EVENTS=ROOT/"repo_events"
LOGS=ROOT/"logs"
CHECKIN_DIR=LOGS/"check-in"
REQUEST_LOG_DIR=LOGS/"request_cycle"
CHECKIN_DOC_RE=re.compile(r"^CID_@R000([A-Z]+)(\d+)\.md$")
MAX_CHECKIN_ROWS=50


def _module_key(value:str)->str:
    return re.sub(r"[^a-z0-9]+","",value.lower())


def _clean_module_name(value:str)->str:
    return value.strip().strip("<>").strip("`").strip()


def _identity_or_none(module_name:str)->dict|None:
    try:
        return load_identity(module_name)
    except Exception:
        return None


def _build_module_aliases()->dict[str,str]:
    aliases={}
    modules_dir=ROOT/"modules"
    if modules_dir.exists():
        for entry in modules_dir.iterdir():
            if entry.is_dir():
                aliases[_module_key(entry.name)]=entry.name
    try:
        routing=load_registry()
        for module_name in routing.values():
            if isinstance(module_name,str):
                aliases[_module_key(module_name)]=module_name
    except Exception:
        pass
    return aliases


def resolve_module_name(target:str|None)->tuple[str|None,str|None]:
    if not target:
        return None,None
    cleaned=_clean_module_name(target)
    if not cleaned:
        return None,None
    if _identity_or_none(cleaned):
        return cleaned,None
    aliases=_build_module_aliases()
    mapped=aliases.get(_module_key(cleaned))
    if mapped and _identity_or_none(mapped):
        return mapped, f"normalized target_module '{target}' -> '{mapped}'"
    return cleaned, f"target_module '{target}' has no known identity manifest; fallback runtime contract will be used"


def _next_alpha(value:str)->str:
    chars=list(value)
    i=len(chars)-1
    while i>=0 and chars[i]=="Z":
        chars[i]="A"; i-=1
    if i<0:
        return "A"*(len(value)+1)
    chars[i]=chr(ord(chars[i])+1)
    return "".join(chars)


def _next_doc_id(letter:str,number:int)->tuple[str,int]:
    if number<50:
        return letter,number+1
    return _next_alpha(letter),1


def _extract_last_entry_no(content:str)->int:
    matches=[int(no) for no in re.findall(r"•\s*NO\.(\d+)\s*:",content)]
    return max(matches) if matches else 0


def _select_checkin_doc(base_dir:Path)->tuple[Path,str,int,int]:
    base_dir.mkdir(parents=True,exist_ok=True)
    docs=[]
    for path in sorted(base_dir.glob("CID_@R000*.md")):
        match=CHECKIN_DOC_RE.match(path.name)
        if not match:
            continue
        letter,number=match.group(1),int(match.group(2))
        row=_extract_last_entry_no(path.read_text(encoding="utf-8"))
        docs.append((letter,number,row,path))
    if not docs:
        doc_id="CID_@R000A1"
        path=base_dir/f"{doc_id}.md"
        return path,doc_id,0,1
    docs.sort(key=lambda item:(len(item[0]),item[0],item[1]))
    letter,number,row,path=docs[-1]
    if row>=MAX_CHECKIN_ROWS:
        n_letter,n_number=_next_doc_id(letter,number)
        doc_id=f"CID_@R000{n_letter}{n_number}"
        return base_dir/f"{doc_id}.md",doc_id,0,1
    doc_id=f"CID_@R000{letter}{number}"
    return path,doc_id,row,row+1


def append_checkin_entry(*,request_name:str,person:str,operation:bool,suggestions:str,timestamp:str)->dict:
    doc_path,doc_id,last_no,next_no=_select_checkin_doc(CHECKIN_DIR)
    if not doc_path.exists():
        header=(
            f"DOCS - ID : {doc_id}\n\n"
            "DOCS - REQUEST CHECK-IN SHEET\n"
            "---\n"
        )
        doc_path.write_text(header,encoding="utf-8")
    content=doc_path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content+="\n"
    block=(
        f"• NO.{next_no} : {request_name}\n"
        f"• DATE : {timestamp}\n"
        f"• Person : {person}\n"
        f"• Operation : {'ทรู' if operation else 'เฟล'}\n"
        f"• Suggestions : {suggestions}\n"
        "---\n"
    )
    doc_path.write_text(content+block,encoding="utf-8")
    return {"doc_id":doc_id,"entry_no":next_no,"path":str(doc_path.relative_to(ROOT))}


def write_request_log(*,request_id:str,target_module:str,status:str,checkin:dict,suggestion:str)->str:
    REQUEST_LOG_DIR.mkdir(parents=True,exist_ok=True)
    path=REQUEST_LOG_DIR/f"{safe_id(request_id)}.md"
    path.write_text(
        "# Request Cycle Log\n\n"
        f"- request_id: `{request_id}`\n"
        f"- target_module: `{target_module}`\n"
        f"- status: `{status}`\n"
        f"- checkin_doc: `{checkin['doc_id']}`\n"
        f"- checkin_entry: `{checkin['entry_no']}`\n"
        f"- checkin_path: `{checkin['path']}`\n"
        "- suggestion:\n\n"
        "```text\n"
        f"{suggestion}\n"
        "```\n",
        encoding="utf-8",
    )
    return str(path.relative_to(ROOT))

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
    try:
        meta["_request_file"]=str(path.relative_to(ROOT))
    except ValueError:
        meta["_request_file"]=str(path)
    meta["_request_text"]=text
    return meta

def safe_id(value:str)->str:
    return re.sub(r"[^A-Za-z0-9_.-]+","-",value).strip("-")

def already_done(rid:str)->bool:
    path=RESULTS/f"{safe_id(rid)}_RESULT.json"
    if not path.exists():
        return False
    try:
        envelope=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError):
        return False
    status=str(envelope.get("runtime_result",{}).get("status") or "").upper()
    return status == "COMPLETED"

def process(path:Path)->dict:
    req=parse_request(path)
    rid=str(req.get("request_id") or path.stem)
    task=str(req.get("task_keyword") or "general").strip()
    requested_target=str(req.get("target_module") or "").strip()
    target, target_warning=resolve_module_name(requested_target)
    if not target:
        try:
            target=route_task(task)["assigned_module"]
        except Exception:
            target="Fallback"

    # A named target is not rejected because another module is the preferred route.
    # Identity/capability stays with the executing module; substitution is traceable.
    manifest=_identity_or_none(target) or {"display_name":target,"status":"unknown","responsibilities":[]}
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
        "request_text": req["_request_text"],
        "observations": [req["_request_text"]],
      },
      "_request_file": req["_request_file"],
      "request_text": req["_request_text"],
      "observations": [req["_request_text"]],
    }
    plan={
      "task":task,
      "kind":task,
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
    operation=bool(result.get("status")=="COMPLETED")
    suggestion=result.get("output") or result.get("error") or "processed"
    person=_clean_module_name(str(req.get("requester") or "BBXDOO")) or "BBXDOO"
    checkin=append_checkin_entry(
        request_name=rid,
        person=person,
        operation=operation,
        suggestions=str(suggestion).strip(),
        timestamp=result.get("time") or now(),
    )
    request_log_path=write_request_log(
        request_id=rid,
        target_module=target,
        status=str(result.get("status") or "FAILED"),
        checkin=checkin,
        suggestion=str(suggestion).strip(),
    )

    # Direct dispatch preserves an explicit target_module, so mirror engine_v2.run()
    # memory persistence here instead of routing through execution_plan(task).
    try:
        add_memory(
            source=target if result.get("status") != "FAILED" else "runtime",
            topic=task,
            content=json.dumps(result.get("agent_result", result), ensure_ascii=False, sort_keys=True),
            tags=["runtime", "request_cycle", str(result.get("status", "unknown")).lower()],
            score=5 if result.get("status") == "COMPLETED" else 1,
            record_type="runtime_result",
        )
    except Exception as memory_exc:
        result["memory_warning"] = str(memory_exc)

    RESULTS.mkdir(parents=True,exist_ok=True); EVENTS.mkdir(parents=True,exist_ok=True)
    envelope={
      "request_id":rid,"source_request":req["_request_file"],"target_module":target,
      "target_module_requested":requested_target or None,
      "target_resolution_warning":target_warning,
      "preferred_module":preferred,"executed_by":target,
      "substitution":bool(preferred and preferred != target),
      "task_keyword":task,"runtime_result":result,
      "artifact_paths":result.get("artifacts",[]),
      "checkin":checkin,
      "request_log":request_log_path,
      "final_signoff_required":bool(req.get("final_signoff_required",True)),
      "closed":False,"mutated":bool(result.get("agent_result",{}).get("mutated",False)),
      "review":True,
    }
    rp=RESULTS/f"{safe_id(rid)}_RESULT.json"
    rp.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ep=EVENTS/f"{safe_id(rid)}_EXECUTION.md"
    ep.write_text(
      f"# Request Execution Event\n\n- request_id: `{rid}`\n- source: `{req['_request_file']}`\n"
      f"- requested/executed_by: `{target}`\n- preferred route: `{preferred or 'none'}`\n"
      f"- substitution: `{str(bool(preferred and preferred != target)).lower()}`\n"
      f"- task: `{task}`\n- status: `{result.get('status')}`\n"
      f"- trace_id: `{result.get('trace_id')}`\n- result: `{rp.relative_to(ROOT)}`\n"
      f"- final_signoff_required: `{str(bool(req.get('final_signoff_required',True))).lower()}`\n"
      "- closed: `false`\n",
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
            if probe.get("request_id") and probe.get("task_keyword"):
                paths.append(candidate)
    if not args.pending and not args.request: ap.error("use --request or --pending")
    rc=0
    for p in paths:
      try: print(json.dumps(process(p),ensure_ascii=False))
      except Exception as e:
        rc=1; print(json.dumps({"status":"FAILED","request":str(p.relative_to(ROOT)),"error":str(e)},ensure_ascii=False))
    raise SystemExit(rc)
if __name__=="__main__": main()
