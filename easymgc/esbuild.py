import os, sys, glob, shutil
import re

def update_ebuild(e_portage_root, es_portage_root, pkg_name):
    src = os.path.join(e_portage_root, pkg_name)
    dest = os.path.join(es_portage_root, pkg_name)
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    if os.path.exists(dest):
        print 'EXIT: dest dir/file exists %s' % dest
    else:
        print 'copy from %s to %s' % (src, dest)
        shutil.copytree(src, dest)
    return True

def clean_ebuild(valid_ebuild):
    fname = os.path.basename(valid_ebuild)
    fpath = os.path.dirname(valid_ebuild)

    for v in glob.glob(fpath+'/*.ebuild'):
        if v != valid_ebuild:
            print 'Remove unuse patch file %s' % v
            os.remove(v)

    for n in ('Manifest', 'metadata.xml', 'ChangeLog'):
        v = os.path.join(fpath, n)
        if os.path.exists(v):
            print 'Remove file: %s' % v
            os.remove(v)

    patch_lines = []
    with open(valid_ebuild) as f:
        content = f.readlines()
        for s in range(len(content)):
            line = content[s].strip()
            if line.find('.patch') >= 0:
                patch_lines.append(content[s])

    ptail_lst = []
    for line in patch_lines:
        line = line.strip(' \\\n')
        ptail = re.search(r'([_\.\d\w-]*\.patch)', line).groups()[0]
        ptail_lst.append(ptail)

    def is_used_file(fn):
        ret = False
        for ptail in ptail_lst:
            if fn.endswith(ptail):
                ret = True
                break
        return ret
    files_path = fpath+'/files'
    if os.path.exists(files_path):
        for f in glob.glob(files_path+'/*'):
            if not is_used_file(f) and f.endswith('.patch'):
                if os.path.isfile(f):
                    print 'Remove unused file %s' % f
                    os.remove(f)
                else:
                    print '!Can not clean dir(%s) in files' % f

        if os.listdir(files_path) == []:
            print 'Remove empty directory %s' % files_path
            os.removedirs(files_path)
    return True

