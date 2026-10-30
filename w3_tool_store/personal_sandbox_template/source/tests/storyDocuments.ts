import assert from 'node:assert/strict';
import { readTextDocument, MAX_DOCUMENT_BYTES } from '../core/documentFiles';
import { createEmptyProject } from '../core/project';
import { buildBackup, parseBackup, saveStory, getStory } from '../core/storage';

const memory = new Map<string, string>();
(globalThis as any).localStorage = {
  getItem: (key: string) => memory.get(key) ?? null,
  setItem: (key: string, value: string) => memory.set(key, value),
  removeItem: (key: string) => memory.delete(key)
};
const original = '# Astrology\n\n| ราศี | ธาตุ |\n| --- | --- |\n| เมษ | ไฟ |\n';
const imported = await readTextDocument(new File(['\uFEFF' + original.replace(/\n/g, '\r\n')], 'Astrology.MD'));
assert.equal(imported.body, original);
assert.equal(imported.title, 'Astrology');
assert.equal(imported.bodyFormat, 'markdown');
assert.equal((await readTextDocument(new File(['ภาษาไทย'], 'บันทึก.txt'))).bodyFormat, 'legacy');
await assert.rejects(readTextDocument(new File(['text'], 'wrong.pdf')), /รองรับไฟล์/);
await assert.rejects(readTextDocument(new File([new Uint8Array(MAX_DOCUMENT_BYTES + 1)], 'large.md')), /4 MB/);
await assert.rejects(readTextDocument(new File([new Uint8Array([0xc3, 0x28])], 'bad.md')), /UTF-8/);
await assert.rejects(readTextDocument(new File(['a\u0000b'], 'binary.txt')), /UTF-8/);
for (const kind of ['library', 'bookcraft', 'concept'] as const) {
  const project = createEmptyProject(`doc-${kind}`, kind, kind);
  project.storyNodes = [
    { nodeId: 'old', type: 'NarrativeBlock', body: '[size=18]เดิม[/size]', choices: [{ label: 'ต่อไป', toNodeId: 'new' }] },
    { nodeId: 'new', type: 'NarrativeBlock', title: imported.title, body: imported.body, bodyFormat: imported.bodyFormat, choices: [] }
  ];
  assert.equal(saveStory(project), true);
  const restored = parseBackup(buildBackup(getStory(project.storyId)!))!.story;
  assert.equal(restored.storyNodes[0].body, '[size=18]เดิม[/size]');
  assert.equal(restored.storyNodes[0].choices![0].toNodeId, 'new');
  assert.equal(restored.storyNodes[1].body, original);
  assert.equal(restored.storyNodes[1].bodyFormat, 'markdown');
  assert.equal(restored.projectKind, kind);
}
assert.equal(getStory('doc-library')!.storyId, 'doc-library');
console.log('Story files: UTF-8/BOM/CRLF, invalid files, size bounds, legacy choices and three-mode backup round trips passed');
