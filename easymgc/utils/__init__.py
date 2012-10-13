import sys, shlex, string
from easymgc import _unicode_encode, _unicode_decode
from easymgc.utils import printer
from easymgc.localization import _

class Logger(object):
    DEBUG     = 0x10000
    INFO      = 0x01000
    WARN      = 0x00100
    ERROR     = 0x00010
    EXCEPTION = 0x00001
    DISPLAY   = 0x01111
    def __init__(self):
        pass

    def d(self, msg):
        self._log(Logger.DEBUG, msg)

    def i(self, msg):
        self._log(Logger.INFO, msg)

    def e(self, msg):
        self._log(Logger.ERROR, msg)

    def w(self, msg):
        self._log(Logger.WARN, msg)

    def exception(self, msg):
        self._log(Logger.EXCEPTION, msg)

    def success(self, msg):
        self._log(Logger.INFO, msg+'  ;-)')

    def failed(self, msg):
        self._log(Logger.ERROR, msg+' :(')

    def _log(self, tag, msg):
        # TODO: do log
        #print '%s\t%s' % (tag, msg)
        if not (tag & Logger.DISPLAY):
            return
        msg += '\n'
        if tag & Logger.DEBUG:
            printer.d(msg)
        elif tag & Logger.INFO:
            printer.i(msg)
        elif tag & Logger.WARN:
            printer.w(msg)
        elif tag & Logger.ERROR:
            printer.e(msg)
        elif tag & Logger.ERROR:
            printer.exception(msg)
            printer.beep()

logger = Logger()

def shlex_split(s):
    """
    This is equivalent to shlex.split, but if the current interpreter is
    python2, it temporarily encodes unicode strings to bytes since python2's
    shlex.split() doesn't handle unicode strings.
    """
    convert_to_bytes = sys.hexversion < 0x3000000 and not isinstance(s, bytes)
    if convert_to_bytes:
        s = _unicode_encode(s)
    rval = shlex.split(s)
    if convert_to_bytes:
        rval = [_unicode_decode(x) for x in rval]
    return rval

#cache expansions of constant strings
cexpand={}
def varexpand(mystring, mydict=None):
    if mydict is None:
        mydict = {}
    newstring = cexpand.get(" "+mystring, None)
    if newstring is not None:
        return newstring

    """
    new variable expansion code.  Preserves quotes, handles \n, etc.
    This code is used by the configfile code, as well as others (parser)
    This would be a good bunch of code to port to C.
    """
    numvars=0
    mystring=" "+mystring
    #in single, double quotes
    insing=0
    indoub=0
    pos=1
    newstring=" "
    while (pos<len(mystring)):
        if (mystring[pos]=="'") and (mystring[pos-1]!="\\"):
            if (indoub):
                newstring=newstring+"'"
            else:
                newstring += "'" # Quote removal is handled by shlex.
                insing=not insing
            pos=pos+1
            continue
        elif (mystring[pos]=='"') and (mystring[pos-1]!="\\"):
            if (insing):
                newstring=newstring+'"'
            else:
                newstring += '"' # Quote removal is handled by shlex.
                indoub=not indoub
            pos=pos+1
            continue
        if (not insing):
            #expansion time
            if (mystring[pos]=="\n"):
                #convert newlines to spaces
                newstring=newstring+" "
                pos=pos+1
            elif (mystring[pos]=="\\"):
                # For backslash expansion, this function used to behave like
                # echo -e, but that's not needed for our purposes. We want to
                # behave like bash does when expanding a variable assignment
                # in a sourced file, in which case it performs backslash
                # removal for \\ and \$ but nothing more. It also removes
                # escaped newline characters. Note that we don't handle
                # escaped quotes here, since getconfig() uses shlex
                # to handle that earlier.
                if (pos+1>=len(mystring)):
                    newstring=newstring+mystring[pos]
                    break
                else:
                    a = mystring[pos + 1]
                    pos = pos + 2
                    if a in ("\\", "$"):
                        newstring = newstring + a
                    elif a == "\n":
                        pass
                    else:
                        newstring = newstring + mystring[pos-2:pos]
                    continue
            elif (mystring[pos]=="$") and (mystring[pos-1]!="\\"):
                pos=pos+1
                if mystring[pos]=="{":
                    pos=pos+1
                    braced=True
                else:
                    braced=False
                myvstart=pos
                validchars=string.ascii_letters+string.digits+"_"
                while mystring[pos] in validchars:
                    if (pos+1)>=len(mystring):
                        if braced:
                            cexpand[mystring]=""
                            return ""
                        else:
                            pos=pos+1
                            break
                    pos=pos+1
                myvarname=mystring[myvstart:pos]
                if braced:
                    if mystring[pos]!="}":
                        cexpand[mystring]=""
                        return ""
                    else:
                        pos=pos+1
                if len(myvarname)==0:
                    cexpand[mystring]=""
                    return ""
                numvars=numvars+1
                if myvarname in mydict:
                    newstring=newstring+mydict[myvarname]
            else:
                newstring=newstring+mystring[pos]
                pos=pos+1
        else:
            newstring=newstring+mystring[pos]
            pos=pos+1
    if numvars==0:
        cexpand[mystring]=newstring[1:]
    return newstring[1:]

