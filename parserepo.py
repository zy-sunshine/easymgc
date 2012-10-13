import os, sys
from easymgc.process import spawn
from easymgc.utils import _, logger
from easymgc import checksum
from xml.dom.minidom import parse

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

from easymgc.utils import shlex_split, varexpand
class Downloader(object):
    def __init__(self):
        logger.d('Init Downloader')
        self.FETCHCOMMAND='wget -t 3 -T 60 --passive-ftp -O "${DISTDIR}/${FILE}" "${URI}"'

    def fetch(self, uri, distdir, myfile=None):
        if myfile is None:
            myfile = os.path.basename(uri)

        variables = {
            "DISTDIR": distdir,
            "URI":     uri,
            "FILE":    myfile
        }
        myfetch = shlex_split(self.FETCHCOMMAND)
        myfetch = [varexpand(x, mydict=variables) for x in myfetch]
        myret = self._spawn_fetch(myfetch)
        return myret

    def _spawn_fetch(self, args, **kwargs):
        """
        Spawn a process with appropriate settings for fetching, including
        userfetch and selinux support.
        """

        # Redirect all output to stdout since some fetchers like
        # wget pollute stderr (if portage detects a problem then it
        # can send it's own message to stderr).
        if "fd_pipes" not in kwargs:

            kwargs["fd_pipes"] = {
                0 : sys.stdin.fileno(),
                1 : sys.stdout.fileno(),
                2 : sys.stdout.fileno(),
            }

        spawn_func = spawn
        rval = spawn_func(args, env=os.environ, **kwargs) # NOTE: portage use --> env=settings.environ()
        return rval

class DownloadManager(object):
    def __init__(self):
        self._dl = Downloader()
        self.digest_map = {}
        self.digest_types = checksum.get_valid_checksum_keys()

    def checksum(self, _file, _type='SHA256', silent=False):
        if _type not in self.digest_types:
            if not silent:
                logger.w(_('Digest(%s) can only be %s') % (_type, ' '.join(self.digest_types)))
            return False

        file_digests = self.digest_map.get(_file)
        if file_digests is None:
            if not silent:
                logger.w(_('Can not find file digest information %s') % _file)
            return False

        digest = file_digests.get(_type)
        if digest is None:
            if not silent:
                logger.w(_('Can not find %s digest from file %s') % (_type, _file))
            return False

        calc_digest = checksum.perform_checksum(_file, _type)[0]
        if digest != calc_digest:
            if not silent:
                logger.failed(_('Digest checksum failed'))
                logger.i(_('Origin digest:\t\t%s') % digest)
                logger.i(_('Calculate digest:\t%s') % calc_digest)
            return False

        if not silent:
            logger.success(_('Checksum valid: %s') % _file)
        return True

    def addDigest(self, _file, digest, _type='SHA256'):
        self.digest_map.setdefault(_file, {})[_type] = digest

    def isValid(self, _file, _type='SHA256'):
        return self.checksum(_file, _type)

    def download(self, uri, save_path, digest=None, digest_type='SHA256'):
        r_f = uri
        l_f = save_path
        valid = False
        if digest is not None:
            self.addDigest(l_f, digest, digest_type)

        if os.path.exists(l_f):
            #logger.w(_('Exists: %s') % l_f)
            # Checksum
            if digest is not None:
                if self.checksum(l_f, digest_type, silent=True):
                    valid = True
                else:
                    os.remove(l_f)
            else:
                valid = True

        if not valid:
            # Fetch
            logger.i(_('Start: download %s') % r_f)
            dl_dir, dl_fn = os.path.split(l_f)
            self._dl.fetch(r_f, dl_dir, dl_fn)
            if os.path.exists(l_f):
                logger.success(_('Sucess: download %s') % l_f)
                valid = True
            else:
                logger.failed(_('Failed: download %s') % l_f)

        return valid

class RepoParser(object):
    def __init__(self):
        self.repo_url = 'http://mirrors.163.com/fedora/releases/17/Everything/source'
        self.repo_src = '%s/SRPMS' % self.repo_url
        self.repodata_l = '%s/repodata' % self.repo_src
        self.r_repomd = '%s/repomd.xml' % self.repodata_l
        self.tmpdir = '%s/tmp' % ROOT_PATH
        self.tmp_dl = '%s/download' % self.tmpdir
        self._dlmanager = DownloadManager()

        self.init()
        ret, meta_path = self.dl_repo_meta()
        if ret:
            self.do_pase(meta_path)

    def init(self):
        tmp_lst = [self.tmpdir, self.tmp_dl, ]
        for d in tmp_lst:
            if not os.path.exists(d):
                logger.d('Create: make tmp dir %s' % d)
                os.makedirs(d)

    def dl_repo_meta(self):
        return self.dl_file(self.r_repomd)

    def dl_file(self, uri, digest=None, digest_type='SHA256'):
        r_f = uri
        l_f = '%s/%s' % (self.tmp_dl, os.path.basename(r_f))
        valid = False
        valid = self._dlmanager.download(r_f, l_f, digest, digest_type)
        if valid and digest is not None:
            if self._dlmanager.isValid(l_f):
                valid = True
            else:
                valid = False

        return valid, l_f

    def do_pase(self, meta_path):
        logger.d('do parse %s' % meta_path)
        doc = parse(meta_path)
        for e_data in doc.getElementsByTagName('data'):
            href = e_data.getElementsByTagName('location')[0].getAttribute('href')
            uri = '%s/%s' % (self.repo_src, href)
            e_checksum = e_data.getElementsByTagName('checksum')[0]
            checksum_value = "".join(t.nodeValue for t in e_checksum.childNodes if t.nodeType == t.TEXT_NODE)
            checksum_type = e_checksum.getAttribute('type')
            if not checksum_type or \
                checksum_type.lower() not in (u'sha256', ):
                logger.e(_('Can not get checksum type "%s"') % checksum_type)
            
            logger.d('download %s' % uri)
            ret, l_f = self.dl_file(uri, checksum_value, checksum_type.upper())

if __name__ == '__main__':
    rp = RepoParser()
