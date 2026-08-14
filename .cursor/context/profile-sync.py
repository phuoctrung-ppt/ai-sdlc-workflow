#!/usr/bin/env python3
"""CLI entry — project profile sync from AGENTS.md §0.

Usage:
  python3 .cursor/context/profile-sync.py --from-agents
  python3 .cursor/context/profile-sync.py --detect
  python3 .cursor/context/profile-sync.py --from-agents --root /path/to/project
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow importing sibling modules when run as script
_SYS_DIR = Path(__file__).resolve().parent
if str(_SYS_DIR) not in sys.path:
    sys.path.insert(0, str(_SYS_DIR))

from profile_sync import main

if __name__ == "__main__":
    main()
