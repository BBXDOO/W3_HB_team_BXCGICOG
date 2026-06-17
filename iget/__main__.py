"""Command-line entrypoint for IGET.

Default behavior preserves the v9 PR governance runtime. New subcommands host
v10-preview helper modes such as issue dispatch.
"""

from __future__ import annotations

import sys

from . import main as governance_main
from . import issue_mode


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == "issue":
        return issue_mode.main(argv[1:])
    return governance_main.main()


if __name__ == "__main__":
    raise SystemExit(main())
