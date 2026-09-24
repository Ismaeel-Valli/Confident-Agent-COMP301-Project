"""Package a built release under Toolbox/, excluding installed dependencies and run data."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
destination = Path(sys.argv[1]).resolve()
destination.parent.mkdir(parents=True, exist_ok=True)
excluded = {'node_modules', '.venv', '.verification-venv', '__pycache__', '.git', 'verification-runs'}
files = []
for path in root.rglob('*'):
    relative = path.relative_to(root)
    if not path.is_file() or any(part in excluded for part in relative.parts):
        continue
    if path.suffix in ('.pyc', '.zip') or path.name in ('BUILD_SHA256.json', 'typecheck_output.txt'):
        continue
    if any(part.startswith(('test-temp', 'test_tmp', '.test-temp')) for part in relative.parts):
        continue
    files.append((relative.as_posix(), path.read_bytes()))
files.sort()
manifest = {name: hashlib.sha256(data).hexdigest() for name, data in files}
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in files:
        archive.writestr('Toolbox/' + name, data)
    archive.writestr('Toolbox/BUILD_SHA256.json', json.dumps(manifest, indent=2) + '\n')
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    for name, digest in manifest.items():
        assert hashlib.sha256(archive.read('Toolbox/' + name)).hexdigest() == digest
print(json.dumps({'file': str(destination), 'entries': len(files) + 1, 'bytes': destination.stat().st_size,
                  'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}))
