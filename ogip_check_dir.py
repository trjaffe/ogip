import os
from ogip_check import ogip_check
from ogip_generic_lib import *
from itertools import chain
from ogip_dictionary import ogip_dictionary
from datetime import datetime
import gc

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
        # dictionary that just counts extensions in files of each type
        self.count_extnames={}


    def update(self,dir=None,file=None,statobj=None):
        # Store dictionaries of directories containing dictionaries of
        # files containing status class objects.  Also keeps a running
        # count of types and extensions checked.

        if statobj.status != 0:
            #  Those that cannot be checked:
            dict_add(self.bad, dir, file, statobj)

        elif statobj.tot_errors() == 0 and statobj.tot_warnings() == 0 and statobj.fver == 0:
            #  Those that pass with no warnings even:
            dict_add(self.good, dir, file, statobj)

        elif statobj.tot_errors() == 0 and statobj.fver == 0:
            #  Those that pass with no errors (but maybe warnings):
            dict_add(self.warned, dir, file, statobj)

        else:
            #  Those that have errors, either FITS (verify) or OGIP standards:
           dict_add(self.failed, dir, file, statobj)

        if statobj.otype != 'unknown':  
            #  Add one to the corresponding type
            dict_incr(self.count_types,statobj.otype)
            #  Another level of dictionaries for extension names for each type
            if statobj.otype not in self.count_extnames: self.count_extnames[statobj.otype]={}
            for extn in statobj.extns:
                dict_incr(self.count_extnames[statobj.otype],extn)


    def count_bad(self):
        return sum(len(d) for d in self.bad.itervalues())

    def count_unrecognized(self):
        return sum( sum([f.unrec for f in d.itervalues()]) for d in self.bad.itervalues() )


    def count_fopen(self):
        #  Inner list comprehension returns a list of files and counts fopen errors,
        #  then iterated and summed over all the directories
        return sum( sum([f.fopen for f in d.itervalues()]) for d in self.bad.itervalues() )

    def count_fver_bad(self):
        #  These are either bad (couldn't be checked, fver==2) or
        #  failed (could be checked but with errors, fver=1)
        return sum( sum([f.fver/2 for f in d.itervalues()]) for d in self.bad.itervalues() )

    def count_fver_fixed(self):
        return sum( sum([f.fver for f in d.itervalues()]) for d in self.failed.itervalues() )

    def count_failed(self):
        return sum(len(d) for d in self.failed.itervalues())

    def count_good(self):
        return sum(len(d) for d in self.good.itervalues())

    def count_warned(self):
        return sum(len(d) for d in self.warned.itervalues())

    def count_checked(self):
        return sum(len(d) for d in self.good.itervalues()) + sum(len(d) for d in self.warned.itervalues()) + sum(len(d) for d in self.failed.itervalues())

    def count_missing_key(self,otype,extname,key):
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
                if extname not in fstat.extns:
                    continue
                if key in fstat.extns[extname].MISKEYS:  count+=1
        for d in self.failed.itervalues():
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if extname not in fstat.extns:
                    continue
                if key in fstat.extns[extname].MISKEYS:  count+=1

        return count




def ogip_check_dir(basedir,logdir,ignore,default_type,verbosity):
    """

    Traverses the given base directory and for all files found beneath:

    - checks if FITS type, and if so

    - runs FITS verify (pyfits), then 

    - runs ogip_check, capturing the output, then 

    - collects statistics on the results, and

    - writes a set of reports.

    """
    summary=ogip_collect()

    print("\nRunning ogip_check_dir with:\n   directory %s\n    logdir %s\n    ignore %s\n" % (basedir,logdir,ignore) )


    # Goes through all contents of root directory
    for dir, subdirs, files in os.walk(basedir, topdown=False):
        if dir in ignore['directories']:
            continue
        for name in [x for x in files if not x.endswith(ignore['suffixes'])]:
            one=os.path.join(dir, name)
            print "\nTIMESTAMP:  " + datetime.now().strftime("%Y-%m-%d %X")

            if logdir:
                logpath= os.path.join(logdir,os.path.relpath(dir,basedir))
                if not os.path.isdir(logpath):  os.makedirs(logpath)
                logfile=os.path.join(logpath,name+".check.log")
                print("CHECKING %s;  see log in %s" % (one, logfile) )
                sys.stdout.flush()
            else:
                logfile=sys.stdout
                print("CHECKING %s" % one)
                sys.stdout.flush()
            #  Returns status that contains both the counts of errors,
            #  warnings, and the logged reports.  
            status=ogip_check(one,None,logfile,verbosity,dtype=default_type)

            #if status.status != 0:
                #print("ERROR:  failed to check file %s;  see log in %s\nContinuing." % (one, logfile) )
            if status.status == 0:
                print("Done.  Found file of type %s with %s errors and %s warnings." % (status.otype, status.tot_errors(),status.tot_warnings() ) )
                sys.stdout.flush()
            # Store the retstat info for the file
            summary.update(dir=dir,file=name,statobj=status)
            gc.collect() # Should be unnecessary but just in case.

    print("\n***************************************************")
    print("Done checking.  Now to summarize:\n")
    print("The total number of files found: %s" % int(summary.count_bad()+summary.count_checked()) )
    print("The total number of files that could not be opened as FITS:  %s" % summary.count_fopen() )
    print("The total number of files whose type could not be recognized:  %s" % summary.count_unrecognized() )
    print("The total number of files that could not be checked for other reasons:  %s" % int(summary.count_bad()-summary.count_fopen()-summary.count_unrecognized()) )
    print("The total number of files that failed FITS verify and could not be checked:  %s" % summary.count_fver_bad() )
    print("The total number of files that failed FITS verify but 'fixed' and checked:  %s" % summary.count_fver_fixed() )
    print("The total number of files checked:  %s" % summary.count_checked() )
    print("The total number of files with no warnings or errors:  %s" % summary.count_good() )
    print("The total number of files with only warnings:  %s" % summary.count_warned() )
    print("The total number of files with errors:  %s" % summary.count_failed() )

    print("")
    for k in summary.count_types:
        print("Checked %s files of type %s" % (summary.count_types[k],k) )

    print("")
    #  Summarize required keywords for each type:
    types=[ 'TIMING', 'SPECTRAL', 'RMF', 'ARF', 'CALDB' ]

    for t in types:
        print("")
        if t not in summary.count_types:
            #  Don't bother to summarize types for which no files were found
            print("Found no files of type %s" % t)
            continue 
        print("Summary of missing required keywords for type %s:" % t)
        dict=ogip_dictionary(t)
        if t == 'CALDB':
            #  CALDB types don't have required extnames.  Any files
            #  checked as CALDB types will store the extn as CALFILE.
            check_extns=['CALFILE']
        else:
            check_extns=dict['EXTENSIONS']['REQUIRED']+ dict['EXTENSIONS']['OPTIONAL']
        for extn in check_extns:
            if extn in summary.count_extnames[t]:
                for k in dict[extn]['KEYWORDS']['REQUIRED']: 
                    if summary.count_missing_key(t,extn,k) > 0:
                        print("    Found %s (out of %s) files have at least one extension %s missing key %s." % (summary.count_missing_key(t,extn,k), summary.count_extnames[t][extn], extn, k) )


    print("\nDone\n")

    return




if __name__== "__main__":
    dir = "."

    status = ogip_check_dir(dir)

    exit(status.status)


