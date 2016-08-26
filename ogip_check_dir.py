import os
from ogip_check import ogip_check
from ogip_generic_lib import *
from itertools import chain



def dict_add(dict,dir,file,statobj):
    #  If an entry for this directory exists, add an entry for the
    #  current file to store the retstat info.  
    if dir not in dict:
        dict[dir]={}
    dict[dir][file]=statobj

def dict_incr(dict,key):
    #  Increment a dictionary key.  
    if key in dict:  dict[key]+=1
    else: dict[key]=1


class ogip_collect:
    """

    For compiling summaries of the results by warnings, errors, etc.

    - Total number of files found:

    """

    def __init__(self):
        # dictionary of directories containing lists of files that
        # could not be checked.
        self.bad={} 
        # dictionary of directories containing files that passed all checks
        self.good={} 
        # dictionary of directories containing files that had only warnings
        self.warned={} 
        # dictionary of directories containing files that had errors
        self.failed={} 
        # dictionary that just counts files found of each type
        self.count_types={}


    def update(self,dir=None,file=None,statobj=None,bad=0):
        if statobj.status != 0:
            dict_add(self.bad, dir, file, statobj)
        elif statobj.ERRORS == 0 and statobj.WARNINGS == 0:
            dict_add(self.good, dir, file, statobj)
        elif statobj.ERRORS == 0:
            dict_add(self.warned, dir, file, statobj)
        else:
            dict_add(self.failed, dir, file, statobj)
        if statobj.otype != 'unknown':  dict_incr(self.count_types,statobj.otype)

    def count_bad(self):
        return sum(len(d) for d in self.bad.itervalues())

    def count_failed(self):
        return sum(len(d) for d in self.failed.itervalues())

    def count_good(self):
        return sum(len(d) for d in self.good.itervalues())

    def count_warned(self):
        return sum(len(d) for d in self.warned.itervalues())

    def count_checked(self):
        return sum(len(d) for d in self.good.itervalues()) + sum(len(d) for d in self.warned.itervalues()) + sum(len(d) for d in self.failed.itervalues())

    def count_missing_key(self,otype,key,extname=None):
        #  Count how many files of a given type are missing a given
        #  keyword.
        #
        #  Don't see a clever pythonic way, so just look through the
        #  whole set of files with either warnings or failures (a
        #  missing keyword could be either) separately.  (Cannot
        #  chain() them, since the same dir key may appear in both
        #  dicts with different lists of files.):
        count=0
        for d in self.warned.itervalues():
            #  Now d is a dictionary of files for a directory.  Check
            #  only those of the right type:
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if key in fstat.MISKEYS:  count+=1
        for d in self.failed.itervalues():
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if key in fstat.MISKEYS:  count+=1

        return count




def ogip_check_dir(basedir,logdir,ignore,verbosity):
    """

    Traverses the given base directory and for all files found beneath:

    - checks if FITS type, and if so

    - runs FITS verify (pyfits), then 

    - runs ogip_check, capturing the output, then 

    - collects statistics on the results, and

    - writes a set of reports.

    """
    summary=ogip_collect()

    # Goes through all contents of root directory
    for dir, subdirs, files in os.walk(basedir, topdown=False):
        if dir in ignore['directories']:
            continue
        for name in [x for x in files if not x.endswith(ignore['suffixes'])]:
            one=os.path.join(dir, name)
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
                print("Done.  Found file of type %s with %s errors and %s warnings.\n" % (status.otype, status.ERRORS,status.WARNINGS))
            # Store the retstat info for the file
            summary.update(dir=dir,file=name,statobj=status)

    print("***************************************************")
    print("Done checking.  Now to summarize:\n")
    print("The total number of files that could not be checked:  %s" % summary.count_bad() )
    print("The total number of files checked:  %s" % summary.count_checked() )
    print("The total number of files with no warnings or errors:  %s" % summary.count_good() )
    print("The total number of files with only warnings:  %s" % summary.count_warned() )
    print("The total number of files with errors:  %s" % summary.count_failed() )

    for k in summary.count_types:
        print("Checked %s files of type %s" % (summary.count_types[k],k) )

    #  Check pairs of types and keywords:
    check={ 'TIMING':['FILTER'], 
            'SPECTRAL':['HDUVERS','ONTIME']}
    for t in check:
        for k in check[t]: 
            print("Found %s (out of %s) files of type %s missing key %s." % (summary.count_missing_key(t,k), summary.count_types[t], t, k) )





    return




if __name__== "__main__":
    dir = "."

    status = ogip_check_dir(dir)

    exit(status.status)


