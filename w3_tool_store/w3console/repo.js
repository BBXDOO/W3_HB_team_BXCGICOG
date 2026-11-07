(() => {
  'use strict';

  const get = id => document.getElementById('repo-' + id);
  const editor = get('editor');
  const tree = get('tree');
  const inSession = new Map();
  const dirty = new Set();
  let repository;
  let selected;
  let opening = 0;

  function element(tag, text) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function button(text, action) {
    const node = element('button', text);
    node.type = 'button';
    node.onclick = action;
    return node;
  }

  async function request(path) {
    const response = await fetch(path);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    return data;
  }

  function status(message) {
    get('status').textContent = message;
  }

  function view(name) {
    get('files').hidden = name !== 'files';
    get('flow').hidden = name !== 'flow';
    for (const tab of document.querySelectorAll('[data-view]')) {
      tab.setAttribute('aria-pressed', String(tab.dataset.view === name));
    }
  }

  function fileButton(path, name) {
    const node = button(name, () => openFile(path));
    node.className = 'repo-file-button';
    node.title = path;
    return node;
  }

  function fillTree(parent, paths) {
    const groups = new Map();
    for (const [path, parts] of paths) {
      if (parts.length === 1) {
        parent.append(fileButton(path, parts[0]));
      } else {
        if (!groups.has(parts[0])) groups.set(parts[0], []);
        groups.get(parts[0]).push([path, parts.slice(1)]);
      }
    }
    for (const [name, children] of groups) {
      const branch = element('details');
      branch.append(element('summary', name));
      branch.addEventListener('toggle', () => {
        if (branch.open && branch.childElementCount === 1) fillTree(branch, children);
      });
      parent.append(branch);
    }
  }

  function draftKey(path) {
    return 'w3console.draft:' + repository.revision + ':' + path;
  }

  function readDraft(path, fallback) {
    if (inSession.has(path)) return inSession.get(path);
    try {
      return localStorage.getItem(draftKey(path)) ?? fallback;
    } catch {
      return fallback;
    }
  }

  function previewMode(on) {
    get('preview-toggle').setAttribute('aria-pressed', String(on));
    get('preview').hidden = !on;
    get('editor-label').hidden = on;
    get('markdown-tools').hidden = on || !selected?.markdown || selected.readonly;
    get('preview-toggle').textContent = on ? 'กลับไปเขียน' : 'ดู Markdown';
    if (on) renderMarkdown(editor.value, get('preview'));
  }

  async function openFile(path, line) {
    const ticket = ++opening;
    try {
      const file = await request('/api/file?' + new URLSearchParams({path}));
      if (ticket !== opening) return;
      const readonly = Number.isInteger(line);
      selected = {path, readonly, markdown: /\.md$/i.test(path)};
      get('document').hidden = false;
      get('path').textContent = path;
      get('location').replaceChildren(document.createTextNode(
        repository.revision.slice(0, 12) + (readonly ? ' · ซอร์ส ณ บรรทัด ' + line : ' · ฉบับร่างบนเครื่อง')
      ));
      editor.value = readonly ? file.text : readDraft(path, file.text);
      editor.readOnly = readonly;
      for (const id of ['paste', 'draft']) get(id).disabled = readonly;
      get('preview-toggle').hidden = !selected.markdown || readonly;
      previewMode(false);
      view('files');
      if (readonly) {
        get('location').append(' ', button('เปิดฉบับร่าง', () => openFile(path)));
        const lines = file.text.split('\n');
        const start = lines.slice(0, line - 1).reduce((size, value) => size + value.length + 1, 0);
        editor.focus({preventScroll:true});
        editor.setSelectionRange(start, start + (lines[line - 1] ?? '').length);
        const height = Number.parseFloat(getComputedStyle(editor).lineHeight);
        editor.scrollTop = Math.max(0, (line - 4) * height);
      } else {
        editor.scrollTop = 0;
        editor.setSelectionRange(0, 0);
      }
      get('document').scrollIntoView({block:'nearest'});
      status('เปิด ' + path);
    } catch (error) {
      if (ticket === opening) status('เปิดไฟล์ไม่ได้ · ' + error.message);
    }
  }

  function recordEdit() {
    if (!selected || selected.readonly) return;
    inSession.set(selected.path, editor.value);
    dirty.add(selected.path);
  }

  function insert(before, after='', placeholder='') {
    if (!selected || selected.readonly) return;
    const {selectionStart, selectionEnd} = editor;
    const value = editor.value.slice(selectionStart, selectionEnd) || placeholder;
    editor.focus();
    // Native insertText preserves the editor's undo history when supported.
    if (!document.execCommand('insertText', false, before + value + after)) {
      editor.setRangeText(before + value + after, selectionStart, selectionEnd, 'end');
    }
    recordEdit();
  }

  function inline(target, text) {
    const matches = /\*\*([^*]+)\*\*|`([^`]+)`|\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
    let cursor = 0;
    for (const match of text.matchAll(matches)) {
      target.append(text.slice(cursor, match.index));
      if (match[1]) target.append(element('strong', match[1]));
      else if (match[2]) target.append(element('code', match[2]));
      else {
        const anchor = element('a', match[3]);
        anchor.href = match[4];
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        target.append(anchor);
      }
      cursor = match.index + match[0].length;
    }
    target.append(text.slice(cursor));
  }

  function renderMarkdown(text, target) {
    target.replaceChildren();
    const lines = text.split(/\r?\n/);
    let code = null;
    let list = null;
    const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(value => value.trim());
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (/^\s*```/.test(line)) {
        if (code) {
          target.append(element('pre', code.join('\n')));
          code = null;
        } else code = [];
        list = null;
      } else if (code) code.push(line);
      else if (line.includes('|') && lines[i + 1]?.includes('|') &&
               cells(lines[i + 1]).every(value => /^:?-{3,}:?$/.test(value))) {
        list = null;
        const table = element('table');
        const addRow = (row, cellTag) => {
          for (const value of cells(row)) inline(table.insertRow().appendChild(element(cellTag)), value);
        };
        addRow(line, 'th');
        i++;
        while (lines[i + 1]?.includes('|') && lines[i + 1].trim()) addRow(lines[++i], 'td');
        target.append(table);
      } else if (/^\s*[-*+] /.test(line)) {
        if (!list) {
          list = element('ul');
          target.append(list);
        }
        const item = element('li');
        inline(item, line.replace(/^\s*[-*+] /, ''));
        list.append(item);
      } else {
        list = null;
        if (!line.trim()) continue;
        const heading = /^(#{1,6})\s+(.+)/.exec(line);
        const paragraph = element(heading ? 'h' + Math.min(6, heading[1].length + 1) : 'p');
        inline(paragraph, heading ? heading[2] : line);
        target.append(paragraph);
      }
    }
    if (code) target.append(element('pre', code.join('\n')));
  }

  async function showFlow() {
    view('flow');
    const target = get('flow');
    target.replaceChildren(element('p', 'กำลังอ่านหลักฐาน…'));
    try {
      const flow = await request('/api/flow');
      target.replaceChildren(element('h3', 'CROLL · สายตรวจสัญญา'));
      target.append(element('p', 'ความสัมพันธ์จากซอร์ส · เลือกจุดเพื่อเปิดบรรทัดหลักฐาน'));
      for (const step of flow.steps) {
        const row = element('div');
        row.className = 'repo-step';
        if (step.source) {
          row.append(button(step.label, () => openFile(step.source.path, step.source.line)));
          row.append(element('p', step.relation));
        } else {
          row.append(element('p', step.label + ' · ยังยืนยันไม่ได้'));
          row.append(element('p', step.unknown));
        }
        target.append(row);
      }
      target.append(element('h3', 'ผลทดสอบในเครื่อง'));
      if (flow.run) {
        target.append(element('p', flow.run.status + ' · ' + flow.run.time));
        target.append(element('pre', flow.run.output));
      } else {
        target.append(element('p', 'ยังไม่มีผลรันที่ตรงกับ Git revision นี้'));
      }
    } catch (error) {
      target.replaceChildren(element('p', 'เปิดความสัมพันธ์ไม่ได้ · ' + error.message));
    }
  }

  for (const tab of document.querySelectorAll('[data-view]')) {
    tab.onclick = () => tab.dataset.view === 'flow' ? showFlow() : view('files');
  }
  get('search').oninput = event => {
    if (!repository) return;
    const query = event.target.value.trim().toLowerCase();
    tree.replaceChildren();
    if (query) {
      const matches = repository.files.filter(path => path.toLowerCase().includes(query));
      tree.append(element('p', matches.length + ' ผลลัพธ์'));
      for (const path of matches.slice(0, 100)) tree.append(fileButton(path, path));
      if (matches.length > 100) tree.append(element('p', 'แสดง 100 รายการแรก · เพิ่มคำค้นเพื่อเจาะจง'));
    } else fillTree(tree, repository.files.map(path => [path, path.split('/')]));
  };
  editor.oninput = recordEdit;
  get('copy').onclick = async () => {
    try {
      const text = editor.value.slice(editor.selectionStart, editor.selectionEnd) || editor.value;
      await navigator.clipboard.writeText(text);
      status('คัดลอกแล้ว');
    } catch {
      editor.focus();
      if (editor.selectionStart === editor.selectionEnd) editor.select();
      status('เลือกข้อความแล้ว · ใช้เมนูคัดลอกของเครื่อง');
    }
  };
  get('paste').onclick = async () => {
    const file = selected;
    try {
      const value = await navigator.clipboard.readText();
      if (selected === file && value) insert(value);
    } catch {
      editor.focus();
      status('แตะค้างในตัวเขียนแล้วเลือกวางจากเมนูของเครื่อง');
    }
  };
  get('draft').onclick = () => {
    try {
      localStorage.setItem(draftKey(selected.path), editor.value);
      dirty.delete(selected.path);
      status('บันทึกร่างในเครื่องแล้ว');
    } catch {
      status('บันทึกร่างไม่ได้ · ใช้ส่งออกไฟล์เพื่อเก็บงาน');
    }
  };
  get('download').onclick = () => {
    const url = URL.createObjectURL(new Blob([editor.value], {type:'text/plain;charset=utf-8'}));
    const link = element('a');
    link.href = url;
    link.download = selected.path.split('/').at(-1);
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  get('preview-toggle').onclick = () => previewMode(get('preview').hidden);
  const marks = {
    heading: ['\n## ', '\n', 'หัวข้อ'], bold: ['**','**','ข้อความ'],
    link: ['[','](https://example.org)','ชื่อลิงก์'],
    table: ['\n| หัวข้อ | รายละเอียด |\n| --- | --- |\n| ', ' | ข้อมูล |\n', 'รายการ'],
    code: ['\n```\n','\n```\n','โค้ด']
  };
  for (const key of document.querySelectorAll('[data-mark]')) {
    key.onclick = () => insert(...marks[key.dataset.mark]);
  }
  window.addEventListener('beforeunload', event => {
    if (dirty.size) {
      event.preventDefault();
      event.returnValue = '';
    }
  });
  request('/api/repo').then(value => {
    repository = value;
    status('Git ' + value.revision.slice(0, 12) + ' · ' + value.files.length + ' ไฟล์');
    fillTree(tree, value.files.map(path => [path, path.split('/')]));
  }).catch(error => status('เปิดรีโป้ไม่ได้ · ' + error.message));
})();
