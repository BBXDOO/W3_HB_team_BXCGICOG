#!/usr/bin/env node
/** Real REA MCP probe. No mocks, no source rewrites, no ownership bypass. */
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { resolve, join, relative } from 'node:path';
import { readFile, writeFile, mkdir, readdir, lstat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  'rea-root': { type: 'string' }, sqlite: { type: 'string' }, javascript: { type: 'string' },
  'source-path': { type: 'string', multiple: true }, output: { type: 'string' }, node: { type: 'string' },
}});
if (!values['rea-root'] || !values.output || (!values.sqlite && !values.javascript)) {
  process.stderr.write('Required: --rea-root PATH --output NEW_DIR and --sqlite PATH or --javascript PATH\n');
  process.exit(1);
}
const reaRoot = resolve(values['rea-root']);
const output = resolve(values.output);
const serverNode = values.node ? resolve(values.node) : process.execPath;
const hash = data => createHash('sha256').update(data).digest('hex');
const save = (name, data) => writeFile(join(output, name), JSON.stringify(data, null, 2) + '\n');
const inputs = [values.sqlite, values.javascript].filter(Boolean).map(p => resolve(p));

async function manifest(root) {
  const files = {};
  async function visit(path) {
    const stat = await lstat(path);
    if (stat.isDirectory()) {
      for (const name of (await readdir(path)).sort()) await visit(join(path, name));
    } else if (stat.isFile()) files[relative(root, path) || '.'] = hash(await readFile(path));
    else files[relative(root, path) || '.'] = { kind: 'unmeasured_non_regular_entry' };
  }
  await visit(root);
  if (root === (values.sqlite ? resolve(values.sqlite) : null)) {
    for (const suffix of ['-wal', '-journal', '-shm']) {
      try { files[suffix] = hash(await readFile(root + suffix)); }
      catch (error) { if (error.code === 'ENOENT') files[suffix] = null; else throw error; }
    }
  }
  return files;
}

await mkdir(output, { recursive: false });
const before = Object.fromEntries(await Promise.all(inputs.map(async p => [p, await manifest(p)])));
const pkg = JSON.parse(await readFile(join(reaRoot, 'package.json'), 'utf8'));
const require = createRequire(join(reaRoot, 'package.json'));
const { Client } = await import(pathToFileURL(require.resolve('@modelcontextprotocol/client')).href);
const { StdioClientTransport } = await import(pathToFileURL(require.resolve('@modelcontextprotocol/client/stdio')).href);
const client = new Client({ name: 'w3-rea-mcp-probe', version: '0.1.0' });
const environment = Object.fromEntries(
  ['PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR', 'SYSTEMROOT', 'WINDIR', 'USERPROFILE', 'APPDATA', 'LOCALAPPDATA']
    .filter(k => process.env[k] !== undefined).map(k => [k, process.env[k]]));
const transport = new StdioClientTransport({ command: serverNode,
  args: [join(reaRoot, 'scripts/rea.mjs'), 'mcp'], env: environment, stderr: 'pipe' });
const summary = { schema: 'w3.rea_mcp_probe.1', observed_at: new Date().toISOString(),
  rea_version: pkg.version, node_version: process.version, connected: false,
  calls: [], limitations: ['Static inspection does not establish W3 runtime correctness.'] };
let stderr = '';
try {
  await client.connect(transport);
  summary.connected = true;
  transport.stderr?.on('data', data => { stderr += data.toString(); });
  const tools = [];
  let cursor;
  do {
    const page = await client.listTools(cursor ? { cursor } : {});
    tools.push(...page.tools); cursor = page.nextCursor;
  } while (cursor);
  summary.tool_count = tools.length;
  await save('catalog.json', { tools: tools.map(t => ({ name: t.name, title: t.title })) });
  async function call(name, args, file) {
    if (!tools.some(t => t.name === name)) throw new Error('Tool not advertised: ' + name);
    const result = await client.callTool({ name, arguments: args });
    await save(file, result);
    let diagnostic;
    if (result.isError) {
      const text = result.content?.find(c => c.type === 'text')?.text;
      try { diagnostic = JSON.parse(text).error; } catch { diagnostic = { message: text }; }
    }
    summary.calls.push({ name, arguments: args, is_error: result.isError === true,
      evidence_id: result.structuredContent?.evidence_id ?? null,
      retained_partial_evidence_id: diagnostic?.details?.partial_observation?.evidence_id ?? null,
      result_file: file, ...(diagnostic ? { diagnostic } : {}) });
  }
  await call('binary_session', {}, 'session.json');
  if (values.sqlite) await call('inspect_sqlite_database', { path: resolve(values.sqlite), table: 'snapshots',
    columns: ['name', 'revision', 'snapshot_id', 'previous_id'], row_limit: 20 }, 'condien-inspection.json');
  if (values.javascript) await call('analyze_javascript_application', { input_path: resolve(values.javascript),
    format: 'directory', ...(values['source-path'] ? { source_paths: values['source-path'] } : {}),
    detail: 'summary' }, 'javascript-inspection.json');
  await call('get_evidence_bundle', { detail: 'complete' }, 'retained-evidence.json');
} catch (error) {
  summary.client_error = { name: error.name, message: error.message };
} finally {
  try { await client.close(); } catch (error) { summary.close_error = error.message; }
  await writeFile(join(output, 'server-stderr.log'), stderr);
  const after = Object.fromEntries(await Promise.all(inputs.map(async p => [p, await manifest(p)])));
  const comparable = !Object.values(before).some(files => Object.values(files).some(v => v !== null && typeof v === 'object'));
  summary.inputs_unchanged = comparable ? JSON.stringify(before) === JSON.stringify(after) : null;
  await save('input-integrity.json', { before, after, complete_regular_file_coverage: comparable });
  summary.state = summary.inputs_unchanged !== true || summary.client_error || summary.close_error
    ? 'STOP' : summary.calls.some(c => c.is_error) ? 'BLOCKED' : 'OBSERVATIONS_COLLECTED';
  // Do not persist process-table rows or ambient environment values.
  const ps = spawnSync('ps', ['-axo', 'pid=,ppid=,pgid=,uid=,stat=,command='],
    { stdio: ['ignore', 'ignore', 'pipe'], encoding: 'utf8' });
  summary.host_ps_probe = { status: ps.status, diagnostic: ps.stderr ?? null };
  await save('summary.json', summary);
}
console.log(JSON.stringify({ state: summary.state, connected: summary.connected, tools: summary.tool_count,
  calls: summary.calls.map(c => ({ name: c.name, is_error: c.is_error })),
  inputs_unchanged: summary.inputs_unchanged, summary: join(output, 'summary.json') }));
process.exitCode = summary.state === 'OBSERVATIONS_COLLECTED' ? 0 : 2;
