import sys

M2K = "/path/to/RFM2RFK"
for path in [M2K]:
    if not path in sys.path:
        sys.path.append(path)


sys.dont_write_bytecode = True

import maya.cmds as cmds

if not cmds.commandPort(":4434", query=True):
    cmds.commandPort(name=":4434")
