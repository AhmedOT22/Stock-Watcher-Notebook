"""JSON persistence: reject corrupt inputs and replace files atomically."""
import json
import os
import tempfile
from pathlib import Path


def load_json(filename, default_data=None):
    path = Path(filename)
    if not path.exists():
        return default_data if default_data is not None else {}
    with path.open(encoding='utf-8') as handle:
        return json.load(handle)


def save_json(filename, data):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix=path.name + '.', suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, indent=2, allow_nan=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
