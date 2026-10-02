import os
import zipfile

os.makedirs('public', exist_ok=True)
zip_path = 'public/w3-idp-studio-source.zip'

exclude_dirs = {'node_modules', '.git', 'dist', '.cache', 'migrated_prompt_history', '__pycache__', 'public'}
exclude_files = {'bun.lock', 'build_zip.py'}

project_files = []
for dirpath, dirnames, filenames in os.walk('.'):
    dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith('.')]
    for f in filenames:
        if f.endswith('.zip') or f in exclude_files:
            continue
        rel = os.path.relpath(os.path.join(dirpath, f), '.')
        project_files.append(rel)

project_files.sort()
print(f"Archiving {len(project_files)} files into {zip_path}...")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for f in project_files:
        zipf.write(f, f)

size_kb = os.path.getsize(zip_path) / 1024
print(f"Successfully generated {zip_path} ({size_kb:.2f} KB)")
