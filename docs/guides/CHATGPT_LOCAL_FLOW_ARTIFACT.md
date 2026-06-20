# ChatGPT Local Flow Artifact

## What this capability does

`ChatGPTAgent` now has one executable local capability: it creates a Markdown flow artifact from a routed W3 task and an optional JSON request file.

It does **not** call OpenAI, any external model, a network API, a shell command, Git, or a deployment target. It must not be described as an AI-model execution.

## Run it

From the repository root:

```sh
python tools/w3run.py flow --request-file modules/ChatGPT/requests/flow_request.example.json
```

The command returns JSON with:

- `status: "COMPLETED"`
- a `trace_id`
- a created artifact path in `modules/ChatGPT/flows/`
- the SHA-256 hash and byte length of the artifact
- explicit review and external-execution boundaries

The generated Markdown artifact records the routed plan, request context, review checklist, and a redacted request payload.

## Request file contract

The request file is one UTF-8 JSON object. The provided example contains the normal fields:

```json
{
  "source": "BBX19",
  "intent": "Describe the requested work",
  "target": "W3",
  "mode": "local_flow_artifact",
  "payload": {
    "requirements": ["..."],
    "constraints": ["..."],
    "expected_outputs": ["..."]
  }
}
```

Do not place patient data, passwords, private keys, session cookies, API tokens, or credentials in this request. Keys resembling common secret fields are redacted in the artifact, but secret handling is not the purpose of this component.

## Truthful runtime status

The runtime now treats an agent without its own `execute()` implementation as `UNAVAILABLE`, not as a completed task. A registered role or a metadata file alone is not enough to produce `COMPLETED`.

At this change point:

- `ChatGPT` can create the local flow artifact described above.
- Other routed runtime agents remain `UNAVAILABLE` until each receives and passes a real executor implementation and artifact-level tests.

## Test

```sh
python -m pytest tests/test_chatgpt_flow_artifact.py
```

The test checks that an artifact is actually written, can be reopened, has the returned SHA-256, and that an unimplemented agent is not reported as completed.
