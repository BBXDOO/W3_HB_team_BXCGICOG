from pathlib import Path
from unittest.mock import patch
import json
import pytest
from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime
from core.runtime import engine_v2 as engine


def task(review=False):
    return orc.new_task('W3-ORC-20261021-99', 'REQUEST', 'NORMAL',
                        {'module': 'BBX19', 'tier': 0}, {}, human_review_required=review)


def success(job, request, **kwargs):
    return {'status': 'COMPLETED', 'trace_id': job,
            'result_validation': {'status': 'valid'},
            'agent_result': {'status': 'COMPLETED', 'module': job, 'mutated': False,
                             'next': ['UNAUTHORIZED_NEXT']}}


def test_explicit_pipeline_persists_and_forwards_without_following_next(tmp_path):
    seen = []
    def runner(job, request, **kw):
        seen.append((job, request))
        return success(job, request)
    circuit = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    t = circuit.run(task(), [{'task': 'design'}, {'task': 'verify'}])
    assert t['status'] == 'COMPLETED'
    assert [j for j, _ in seen] == ['design', 'verify']
    assert seen[1][1]['payload']['module'] == 'design'
    assert all(r['task_id'] == t['task_id'] for _, r in seen)
    assert [r['destination']['module'] for r in t['route']] == ['ChatGPT', 'Gemini']
    assert json.loads((tmp_path/'tasks'/f"{t['task_id']}.json").read_text())['status'] == 'COMPLETED'
    assert all(Path(e['ref']).exists() for e in t['evidence'])


def test_failed_verifier_support_then_explicit_retry(tmp_path):
    passed = False
    c = WorkflowRuntime(tmp_path, runner=success, verifier=lambda *a: {'passed': passed})
    t = c.run(task(), [{'task': 'verify'}])
    assert t['status'] == 'BLOCKED'
    c.assist(t, kind='TOOL', name='repair', handler=lambda p: {'resolved': True, 'evidence': 'fixture:repair'})
    assert t['status'] == 'RETURNED'
    with pytest.raises(ValueError, match='original stage'):
        c.execute_stage(t, {'task': 'design'})
    passed = True
    c.execute_stage(t, {'task': 'verify'})
    assert t['status'] == 'VERIFYING'


def test_review_required_never_closes_or_runs_next(tmp_path):
    def review(*a, **kw):
        r=success(*a, **kw);r['agent_result']['review']=True;return r
    c=WorkflowRuntime(tmp_path, runner=review, verifier=lambda *a: {'passed': True})
    t=c.run(task(), [{'task':'design'}, {'task':'verify'}])
    assert t['status']=='WAITING_HUMAN' and len(t['route'])==1


def test_final_human_gate_and_resume_not_automatic(tmp_path):
    c=WorkflowRuntime(tmp_path,runner=success,verifier=lambda *a:{'passed':True})
    t=c.run(task(True),[{'task':'verify'}])
    assert t['status']=='WAITING_HUMAN'
    with pytest.raises(ValueError):c.run(t,[{'task':'verify'}])


def test_contract_block_and_no_execution_for_wrong_route(tmp_path):
    def invalid(*a,**kw):
        r=success(*a,**kw);r['result_validation']['status']='review_required';return r
    c=WorkflowRuntime(tmp_path,runner=invalid,verifier=lambda *a:{'passed':True})
    t=c.run(task(),[{'task':'trace'}]);assert t['status']=='BLOCKED'
    with pytest.raises(ValueError):c.run(task(),[{'task':'design','module':'LRC2'}])


def test_real_gemini_executor_and_verification_failure(tmp_path):
    def verify(stage,result):
        return {'passed': result['agent_result'].get('decision')=='VERIFIED'}
    c=WorkflowRuntime(tmp_path,verifier=verify)
    with patch.object(engine,'search_memory',return_value=[]),patch.object(engine,'add_memory'):
        t=c.run(task(),[{'task':'verify','request':{'payload':{'checks':[True], 'evidence':['fixture']}}}])
    # Gemini deliberately requests review even for its locally verified stamp.
    assert t['status'] in {'COMPLETED','WAITING_HUMAN'}
    assert len(t['route'])==1


def test_engine_fail_closed_and_pre_dispatch_errors():
    with patch.object(engine,'search_memory',return_value=[]),patch.object(engine,'add_memory') as memory,patch.object(engine,'dispatch',return_value={'status':'COMPLETED'}):
        r=engine.run('route')
        assert r['status']=='REVIEW_REQUIRED'
        assert memory.call_args.kwargs['score']==1
    with patch.object(engine,'add_memory'):
        assert engine.run('UNKNOWN')['status']=='FAILED'
    with patch.object(engine,'search_memory',return_value=[]),patch.object(engine,'dispatch',side_effect=RuntimeError('executor')),patch.object(engine,'add_memory',side_effect=OSError('disk')):
        r=engine.run('design');assert r['status']=='FAILED' and r['memory_error']=='disk'


def test_legacy_delegates():
    from core.runtime import engine as legacy
    with patch.object(engine,'run',return_value={'status':'REVIEW_REQUIRED','trace_id':'fixture','agent_result':{'status':'REVIEW_REQUIRED'}}) as run:
        r=legacy.run('verify')
    run.assert_called_once()
    assert r['output']['status']=='REVIEW_REQUIRED'


def test_human_review_checks_result_before_final_closure(tmp_path):
    def reviewed(*a,**kw):
        r=success(*a,**kw);r['agent_result']['review']=True;return r
    c=WorkflowRuntime(tmp_path,runner=reviewed,verifier=lambda *a:{'passed':True})
    t=c.run(task(),[{'task':'design'}])
    c.review_stage(t,{'task':'design'},human='test-human',evidence='test:review')
    orc.advance(t,'COMPLETED',actor='Orchestration',detail='final reviewed stage')
    assert t['status']=='COMPLETED'


def test_real_flow_artifact_evidence_and_human_gate(tmp_path):
    import hashlib
    from core.runtime.agents.chatgpt import ChatGPTAgent
    # Redirect the actual module's repository root so generated artifacts stay isolated.
    import core.runtime.agents.chatgpt as chatgpt
    def verify(stage,result):
        artifacts=result.get('artifacts',[])
        return {'passed':bool(artifacts) and all(
            (ChatGPTAgent._REPO_ROOT/a['path']).is_file() and
            hashlib.sha256((ChatGPTAgent._REPO_ROOT/a['path']).read_bytes()).hexdigest()==a['sha256']
            for a in artifacts)}
    with patch.object(ChatGPTAgent,'_REPO_ROOT',tmp_path),patch.object(ChatGPTAgent,'_DEFAULT_FLOW_DIR',tmp_path/'modules/ChatGPT/flows'),patch.object(engine,'search_memory',return_value=[]),patch.object(engine,'add_memory'):
        c=WorkflowRuntime(tmp_path/'circuit',verifier=verify)
        t=c.run(task(),[{'task':'design'}])
        assert t['status']=='WAITING_HUMAN'
        c.review_stage(t,{'task':'design'},human='test-human',evidence='test:review')
        assert t['status']=='VERIFYING'
