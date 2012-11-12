import portage

def doebuild(myebuild, mydo, _unused=None, settings=None, debug=0, listonly=0,
    fetchonly=0, cleanup=0, dbkey=None, use_cache=1, fetchall=0, tree=None,
    mydbapi=None, vartree=None, prev_mtimes=None,
    fd_pipes=None, returnpid=False):

    portage.doebuild(myebuild, mydo, _unused, settings, debug, listonly,
        fetchonly, cleanup, dbkey, use_cache, fetchall, tree,
        mydbapi, vartree, prev_mtimes,
        fd_pipes, returnpid)