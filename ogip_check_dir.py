import os
from ogip_check import ogip_check
from ogip_generic_lib import retstat


def ogip_check_dir(basedir,logdir,verbosity):
    """

    Traverses the given base directory and for all files found beneath:

    - checks if FITS type, and if so

    - runs FITS verify (pyfits), then 

    - runs ogip_check, capturing the output, then 

    - collects statistics on the results, and

    - writes a set of reports.

    """


    # Goes through all contents of root directory
    for root, dirs, files in os.walk(basedir, topdown=False):
        for name in [x for x in files if not x.endswith(('.jpg','.txt','.gif','.dat'))]:
            one=os.path.join(root, name)
            #  Assumes no two files with same name, writes logs all in
            #  one place for now.  Remove later if no longer needed.
            logfile=os.path.join(logdir,name+".check.log")
            print("CHECKING %s;  see log in %s" % (one, logfile) )
            #  Returns status that contains both the counts of errors,
            #  warnings, and the logged reports.  
            status=ogip_check(one,None,logfile,verbosity)
            if status.status != 0:
                print("ERROR:  failed to check file %s;  see log in %s\nContinuing.\n" % (one, logfile) )
            else:
                print("Done.  Found %s errors and %s warnings.\n" % (status.ERRORS,status.WARNINGS))

    return 




if __name__== "__main__":
    dir = "."

    status = ogip_check_dir(dir)

    exit(status.status)


