#!/usr/bin/python -O

import sys
import optparse
import signal

def debug_signal(signum, frame):
	import pdb
	pdb.set_trace()
signal.signal(signal.SIGUSR1, debug_signal)

description = "See the ebuild(1) man page for more info"
usage = "Usage: ebuild <ebuild file> <command> [command] ..."
parser = optparse.OptionParser(description=description, usage=usage)

force_help = "When used together with the digest or manifest " + \
	"command, this option forces regeneration of digests for all " + \
	"distfiles associated with the current ebuild. Any distfiles " + \
	"that do not already exist in ${DISTDIR} will be automatically fetched."

parser.add_option("--force", help=force_help, action="store_true", dest="force")
parser.add_option("--color", help="enable or disable color output",
	type="choice", choices=("y", "n"))
parser.add_option("--debug", help="show debug output",
	action="store_true", dest="debug")
parser.add_option("--version", help="show version and exit",
	action="store_true", dest="version")
parser.add_option("--ignore-default-opts",
	action="store_true",
	help="do not use the EBUILD_DEFAULT_OPTS environment variable")
parser.add_option("--skip-manifest", help="skip all manifest checks",
	action="store_true", dest="skip_manifest")

opts, pargs = parser.parse_args(args=sys.argv[1:])

if __name__ == '__main__':
	import os, time
	print os.getpid()
	print opts, pargs
	