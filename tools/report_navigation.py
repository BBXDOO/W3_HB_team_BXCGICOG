"""Readable companion reports with contextual response links.

Immutable executor artifacts (including LRC2 JSON/hash evidence) are preserved.
This publisher writes navigation/report views, not human decisions.
"""
import json
import hashlib
from pathlib import Path
import posixpath
import re
from urllib.parse import quote

MARKER = '<!-- w3-human-response-links -->'
GUIDE = 'BBEX-Core/private/callback/README.md'


def discussion_url(value):
    text = str(value or '').strip()
    if re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/pull/[1-9][0-9]*(?:#[A-Za-z0-9_-]+)?', text):
        return text
    return None


def related_pr(root, request):
    direct = discussion_url(request.get('discussion_url'))
    if direct:
        return direct
    channels = Path(root)/'BBEX-Core/private/callback/channels.json'
    if channels.is_file():
        try:
            entries = json.loads(channels.read_text())
            entry = entries.get(request.get('request_id'), {}) if isinstance(entries, dict) else {}
            return discussion_url(entry.get('discussion_url')) if isinstance(entry, dict) else None
        except (OSError, ValueError):
            return None
    return None


def relative(root, document, target):
    root = Path(root).resolve()
    target_path = (root/target).resolve()
    if not target_path.is_relative_to(root):
        raise ValueError('report link escapes repository')
    return quote(posixpath.relpath(str(target_path.relative_to(root)), str(Path(document).parent)), safe='/')


def footer(root, request, envelope, document):
    result = envelope.get('runtime_result', {})
    status = result.get('status', 'UNKNOWN')
    callback = envelope.get('callback_path') or result.get('callback_path')
    pr = related_pr(root, request)
    lines = [MARKER, '\n---\n', '### ตอบกลับรายงาน\n']
    if status in {'COMPLETED','REJECTED','CANCELLED'} or envelope.get('closed'):
        lines.append(f'วงจรนี้จบที่ `{status}` แล้ว ไม่ต้องตรวจรับซ้ำ\n')
    else:
        lines.append(f'สถานะ `{status}` — ตอบโดยอ้างอิงใบงาน `{envelope["request_id"]}`\n')
        if callback:
            lines.append(f'- [📝 เปิดฟอร์มตอบรายงานนี้]({relative(root, document, callback)})')
        else:
            lines.append('- ฟอร์มยังไม่ถูกเตรียม ใช้ --prepare ตามคู่มือด้านล่าง')
        if pr:
            lines.append(f'- [💬 แสดงความคิดเห็นใน PR ที่เกี่ยวข้อง]({pr})')
            lines.append('\nคอมเมนต์ PR เก็บคำตอบ/หลักฐานไว้ได้ การเปลี่ยนสถานะอัตโนมัติใช้ฟอร์มด้านบน คอมเมนต์อย่างเดียวยังไม่บันทึกคำตัดสินเข้าวงจร\n')
    lines.append(f'- [📑 วิธีตอบและความหมายของคำตอบ]({relative(root, document, GUIDE)})')
    return '\n'.join(lines)+'\n'


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


def publish(root, request, envelope, *, result_path, event_path):
    root = Path(root).resolve()
    result_path, event_path = Path(result_path), Path(event_path)
    report = result_path.with_name(result_path.name.replace('_RESULT.json', '_REPORT.md'))
    document = str(report.relative_to(root))
    envelope['report_path'] = document
    envelope['discussion_url'] = related_pr(root, request)
    result = envelope.get('runtime_result', {})
    lines = [f'# รายงาน {envelope["request_id"]}\n', f'- สถานะ: `{result.get("status", "UNKNOWN")}`',
             f'- [ใบงานต้นทาง]({relative(root, document, (envelope.get("source_request") or request["_request_file"]))})',
             f'- [ผลแบบ JSON]({relative(root, document, str(result_path.relative_to(root)))})',
             '\n## ผลที่บันทึกไว้\n', str(result.get('output') or result.get('error') or 'ดูผลและหลักฐานที่แนบ'),
             '\n## ผลงานและหลักฐาน\n']
    for artifact in result.get('artifacts', []):
        if isinstance(artifact, dict) and artifact.get('path'):
            label = str(artifact['path']).replace('[','').replace(']','')
            lines.append(f'- [{label}]({relative(root, document, artifact["path"])})')
            if artifact.get('kind') == 'w3.lrc2.log_analysis.json':
                source = (root/artifact['path']).resolve()
                if not source.is_relative_to(root):
                    raise ValueError('report source escapes repository')
                try:
                    data = source.read_bytes()
                    if hashlib.sha256(data).hexdigest() != artifact.get('sha256'):
                        lines.append('\n⚠️ ไฟล์รายงานไม่ตรง hash ที่บันทึกไว้ ควรตรวจหลักฐานก่อนใช้ผล\n')
                    else:
                        analysis = json.loads(data)
                        lines.extend(['\n### ผลวิเคราะห์ LRC2\n',
                            f"วิเคราะห์ {analysis['records_total']} รายการ แบ่ง {len(analysis['groups'])} กลุ่มงาน\n",
                            '| สถานะที่บันทึก | จำนวน |', '|---|---:|'])
                        for category, count in analysis['categories'].items():
                            lines.append(f'| {category} | {count} |')
                        lines.append('\nจำนวนนี้เป็นสถานะในประวัติ ไม่รับรองคุณภาพงานหรือโอกาสสำเร็จในอนาคต รายละเอียดและข้อจำกัดทั้งหมดอยู่ในไฟล์ต้นฉบับที่แนบ\n')
                except (OSError, ValueError, KeyError, TypeError):
                    lines.append('\nยังสรุปไฟล์แนบไม่ได้ โปรดตรวจต้นฉบับและหลักฐาน\n')

    if envelope.get('orchestration_evidence'):
        lines.append(f'- [ประวัติวงจรงาน]({relative(root, document, envelope["orchestration_evidence"])})')
    _write(report, '\n'.join(lines)+'\n\n'+footer(root, request, envelope, document))
    if event_path.exists():
        old = event_path.read_text(encoding='utf-8').split(MARKER, 1)[0].rstrip()
        _write(event_path, old+'\n\n'+footer(root, request, envelope, str(event_path.relative_to(root))))
    _write(result_path, json.dumps(envelope, ensure_ascii=False, indent=2)+'\n')
    return document
