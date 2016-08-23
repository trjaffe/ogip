import os
from ogip_check import ogip_check
from ogip_generic_lib import retstat


def ogip_check_dir(basedir,logdir,verbosity):
    """

    Traverses the given base directory and for all files found:

    - checks if FITS type, and if so

    - runs ogip_check, capturing the output, and

    - collects statistics on the results, and

    - writes a set of reports.

    """


    status=retstat(0,[''],0,0)

    # Goes through all contents of root directory
    for root, dirs, files in os.walk(basedir, topdown=False):
        for name in files:
            one=os.path.join(root, name)
            #  Assumes no two files with same name, writes logs all in
            #  one place for now.  Remove later if no longer needed.
            logfile=os.path.join(logdir,name+".check.log")
            this_status=ogip_check(one,None,logfile,verbosity)


    return(status)




if __name__== "__main__":
    dir = "~/"

    status = ogip_check_dir(dir)

    exit(status.status)


