# EVENT_TEMPLATE_CONDIEN_BRIDGE.md

MPCP Event Template / Condien Bridge

Status: ACTIVE DRAFT  
Owner: BBX19  
Scope: event template / Condien lib selection / Paper Pack planning

---

## 1. Purpose

Event is not one type, one shape, or one behavior.

Each event family should have a template that shapes incoming data before MPCP or Condien has to act.

```text
Template reduces guessing.
Condien uses the template to select lib and prepare field.
Paper Pack distributes work inside the event scope.
```

---

## 2. Event template role

An Event Template is the shape that tells the system how data should enter an event.

It may define:

```text
TEMPLATE_ID
EVENT_TYPE
SCOPE
CONTEXT_FIELDS
REQUIRED_PAYLOAD
OPTIONAL_PAYLOAD
CONDIEN_LIBS
ALLOWED_ASSIST
PAPER_PACK_HINT
CROSS_FIELD_HINT
RETURN_TO
END_EVENT
```

The template does not execute.
The template does not replace Paper.
The template only makes the event readable enough that Condien does not need to guess.

---

## 3. Condien bridge

Condien reads the event template and pulls the matching lib / field preparation.

```text
Raw input
→ Event Template
→ Event Instance
→ Condien lib request
→ Paper Pack / Cross-X / Modew assist
→ Result combine
→ LRC2 log
→ End Event
```

Condien should ask:

```text
Which lib should be prepared?
Which field must be shaped?
Which assist route is allowed?
Which boundary must be preserved?
Where should result return?
```

---

## 4. Template example

```json
{
  "TEMPLATE_ID": "EVT:MPCP/LIB.BLUEPRINT",
  "EVENT_TYPE": "MPCP_LIB_BLUEPRINT",
  "SCOPE": "MPCP_LIB_BLUEPRINT_BUILD",
  "CONTEXT_FIELDS": ["MPCP", "LIB", "BLUEPRINT"],
  "REQUIRED_PAYLOAD": ["code_set", "intent", "scope"],
  "OPTIONAL_PAYLOAD": ["risk", "context", "expected_gain"],
  "CONDIEN_LIBS": ["lib_blueprint", "file_boundary", "table_relation", "modew_dynamic"],
  "ALLOWED_ASSIST": ["Table-X", "file.void", "Modew-dynamic"],
  "PAPER_PACK_HINT": "Papers-Pack-A01",
  "CROSS_FIELD_HINT": "Cross-X",
  "RETURN_TO": "MPCP",
  "END_EVENT": 1
}
```

---

## 5. Paper Pack relation

The template may recommend Paper Pack structure, but it should not force every event to split.

Split only when needed:

```text
uncertain
abnormal
malformed
incomplete
needs_more_variables
risk_distribution_needed
parallel_check_needed
other_path_faster
other_path_more_precise
```

---

## 6. Final law

```text
Event Template shapes entry.
Condien prepares field.
Paper Pack distributes only when useful.
Cross-X provides assist field.
Modew helps where capability fits.
MPCP keeps responsibility and trace.
```
