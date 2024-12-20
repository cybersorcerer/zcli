import sys
"""
    Determine if we are on a tty and set Variables
"""
TERMINAL: bool       = False
DEBUG_FG_COLOR: str  = None
INFO_FG_COLOR: str   = None
WARN_FG_COLOR: str   = None
ERROR_FG_COLOR: str  = None
SEVERE_FG_COLOR: str = None

if sys.stdout.isatty():
    TERMINAL: bool = True
    DEBUG_FG_COLOR: str  = 'blue'
    INFO_FG_COLOR: str   = 'green'
    WARN_FG_COLOR: str   = 'yellow'
    ERROR_FG_COLOR: str  = 'magenta'
    SEVERE_FG_COLOR: str = 'red'
    """
        _Clear the screen_
    """
    print(chr(27) + "[2J")
    print(chr(27) + "[1;1f")
