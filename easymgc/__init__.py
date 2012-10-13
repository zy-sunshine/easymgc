import sys

try:
    import sys
    import errno
    if not hasattr(errno, 'ESTALE'):
        # ESTALE may not be defined on some systems, such as interix.
        errno.ESTALE = -1
    import re
    import types

    # Try the commands module first, since this allows us to eliminate
    # the subprocess module from the baseline imports under python2.
    try:
        from commands import getstatusoutput as subprocess_getstatusoutput
    except ImportError:
        from subprocess import getstatusoutput as subprocess_getstatusoutput

    import platform

    # Temporarily delete these imports, to ensure that only the
    # wrapped versions are imported by easymgc internals.
    import os
    del os
    import shutil
    del shutil

except ImportError as e:
    sys.stderr.write("\n\n")
    sys.stderr.write("!!! Failed to complete python imports. These are internal modules for\n")
    sys.stderr.write("!!! python and failure here indicates that you have a problem with python\n")
    sys.stderr.write("!!! itself and thus easymgc is not able to continue processing.\n\n")

    sys.stderr.write("!!! You might consider starting python with verbose flags to see what has\n")
    sys.stderr.write("!!! gone wrong. Here is the information we got for this exception:\n")
    sys.stderr.write("    "+str(e)+"\n\n");
    raise

try:
    import easymgc.proxy.lazyimport
    import easymgc.proxy as proxy
    proxy.lazyimport.lazyimport(globals(),
        'easymgc.checksum',
        'easymgc.checksum:perform_checksum,perform_md5,prelink_capable',
        'easymgc.exception',
        'easymgc.process',
        'easymgc.process:atexit_register,run_exitfuncs',
        #'easymgc.xpak',
    )

except ImportError as e:
    sys.stderr.write("\n\n")
    sys.stderr.write("!!! Failed to complete easymgc imports. There are internal modules for\n")
    sys.stderr.write("!!! easymgc and failure here indicates that you have a problem with your\n")
    sys.stderr.write("!!! installation of easymgc. Please try a rescue easymgc located in the\n")
    sys.stderr.write("!!! easymgc tree under '/usr/easymgc/sys-apps/easymgc/files/' (default).\n")
    sys.stderr.write("!!! There is a README.RESCUE file that details the steps required to perform\n")
    sys.stderr.write("!!! a recovery of easymgc.\n")
    sys.stderr.write("    "+str(e)+"\n\n")
    raise

import os as _os
os = _os
_encodings = {
    'content'                : 'utf_8',
    'fs'                     : 'utf_8',
    'merge'                  : 'utf_8',
    'repo.content'           : 'utf_8',
    'stdio'                  : 'utf_8',
}
_python_interpreter = os.path.realpath(sys.executable)
if sys.hexversion >= 0x3000000:
    def _unicode_encode(s, encoding=_encodings['content'], errors='backslashreplace'):
        if isinstance(s, str):
            s = s.encode(encoding, errors)
        return s

    def _unicode_decode(s, encoding=_encodings['content'], errors='replace'):
        if isinstance(s, bytes):
            s = str(s, encoding=encoding, errors=errors)
        return s
else:
    def _unicode_encode(s, encoding=_encodings['content'], errors='backslashreplace'):
        if isinstance(s, unicode):
            s = s.encode(encoding, errors)
        return s

    def _unicode_decode(s, encoding=_encodings['content'], errors='replace'):
        if isinstance(s, bytes):
            s = unicode(s, encoding=encoding, errors=errors)
        return s
