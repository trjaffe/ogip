import os
from ogip_check import ogip_check
from ogip_generic_lib import *
from itertools import chain
from ogip_dictionary import ogip_dictionary
from datetime import datetime
import gc
import json
import inspect

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
        # could not be checked for a number of reasons.
        self.bad={} 
        # dictionary of directories containing files that passed all checks
        self.good={} 
        # dictionary of directories containing files that had only warnings
        self.warned={} 
        # dictionary of directories containing files that had STANDARDS errors,
        #  either FITS standards or OGIP.  
        self.failed={} 
        # dictionary that just counts files found of each type
        self.count_types={}
        # dictionary that just counts extensions in files of each type
        self.count_extnames={}
        self.count_unrec_extnames={}
        # dictionary containing unrecognized extensions found
        self.unrec_extnames={}

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
                
            for extn in statobj.unrec_extns:
                dict_incr(self.unrec_extnames,extn)


        else:
            # For unrecognized files, list and count unrecognized
            # extensions.  Note that in this case, statobj.extns is a
            # simple list instead of a dictionary pointing to the
            # statinfo for that extn.
            for extn in statobj.extns:
                #  Since you get here with unopened files, for
                #  example, and we don't want to count the "none"s as
                #  unrecognized extension names.
                if extn != 'none':  
                    dict_incr(self.unrec_extnames,extn)

    def count_bad(self):
        return sum(len(d) for d in self.bad.itervalues())

    def count_unrecognized(self):
        return sum( sum([f.unrec for f in d.itervalues()]) for d in self.bad.itervalues() )


    def count_fopen(self):
        #  Inner list comprehension returns a list of files and counts fopen errors,
        #  then iterated and summed over all the directories
        return sum( sum([f.fopen for f in d.itervalues()]) for d in self.bad.itervalues() )

    def count_fver_bad(self):
        #  These are always bad (couldn't be checked, fver==2).  (But not all bad have fver==2 so check.)  
        return sum( sum([f.fver/2 for f in d.itervalues() if f.fver == 2]) for d in self.bad.itervalues() )

    def count_fver_fixed(self):
        #  Want to count all those that were fixable fverify problems,
        #  i.e., with fver==1, whether they were checked after (which
        #  would put them in the "failed" category) or not ("bad"
        #  category):
        return sum( sum([f.fver for f in d.itervalues() if f.fver == 1]) for d in self.failed.itervalues() ) + \
               sum( sum([f.fver for f in d.itervalues() if f.fver == 1]) for d in self.bad.itervalues() )

    def count_failed(self):
        #  Were checked but failed in the sense of violating either
        #  FITS or OGIP standards
        return sum(len([f for f in d.itervalues() if f.vonly==False]) for d in self.failed.itervalues())

    def count_good(self):
        return sum(len([f for f in d.itervalues() if f.vonly==False]) for d in self.good.itervalues())

    def count_warned(self,level=None):
        # 
        count=0
        for d in self.warned.itervalues():
            for f in d.itervalues():
                for e in f.extns.itervalues():
                    if e.WARNINGS[level]>0:
                        count+=1
                        break # Only count once for the file even if multiple extensions have level=level warnings.
        return count
        

    def count_checked(self):
        return (  sum(len([f for f in d.itervalues() if f.vonly==False]) for d in self.good.itervalues()) 
                + sum(len([f for f in d.itervalues() if f.vonly==False]) for d in self.warned.itervalues()) 
                + sum(len([f for f in d.itervalues() if f.vonly==False]) for d in self.failed.itervalues())
        )
    def count_verified(self):
        return (  sum(len([f for f in d.itervalues() if f.vonly==True]) for d in self.good.itervalues()) 
                + sum(len([f for f in d.itervalues() if f.vonly==True]) for d in self.warned.itervalues()) 
                + sum(len([f for f in d.itervalues() if f.vonly==True]) for d in self.failed.itervalues())
        )

    def count_missing_key(self,otype,extname,key):
        #  Count how many files of a given type are missing a given
        #  keyword.
        #
        #  Don't see a clever pythonic way, so just look through the
        #  whole set of files with failures (a missing keyword is an
        #  error case):
        count=0
        for d in self.failed.itervalues():
            #  Now d is a dictionary of files for a directory.  Check
            #  only those of the right type:
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if extname not in fstat.extns:
                    continue
                if key in fstat.extns[extname].MISKEYS:  count+=1
        return count

    def count_missing_col(self,otype,extname,col):  
        count=0
        for d in self.warned.itervalues():
            #  Now d is a dictionary of files for a directory.  Check
            #  only those of the right type:
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if extname not in fstat.extns:
                    continue
                if col in fstat.extns[extname].MISCOLS:  count+=1
        for d in self.failed.itervalues():
            for fstat in (dd for dd in d.itervalues() if dd.otype == otype):
                if extname not in fstat.extns:
                    continue
                if col in fstat.extns[extname].MISCOLS:  count+=1

        return count







def ogip_check_dir(basedir,logdir,meta_key,default_type,verbosity):
    """

    Traverses the given base directory and for all files found beneath:

    - checks if FITS type, and if so

    - runs FITS verify (pyfits), then 

    - runs ogip_check, capturing the output, then 

    - collects statistics on the results, and

    - writes a set of reports.

    """

    #  Get from meta data lists of suffixes and directories to ignore:
    igfile=os.path.join(os.path.dirname(__file__),("meta_%s.json"%meta_key))
    try:
        meta=json.load( open(igfile) )
    except:
        print("ERROR:  the meta data key %s does not correspond to a known meta-data JSON dictionary in %s." % (meta_key,os.path.dirname(__file__)) )
        raise
    ignore={
        'suffixes':tuple(meta["ignore"]["suffixes"]),
        'directories':tuple(meta["ignore"]["directories"]),
    }

    #  Object that holds summary data and methods.  
    summary=ogip_collect()

    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    print("Running %s with" % inspect.getframeinfo(frame)[2])
    for i in args:
        print("    %s = %s" % (i, values[i]))

    # Goes through all contents of root directory
    for dir, subdirs, files in os.walk(basedir, topdown=False,followlinks=True):
        if os.path.split(dir)[1].startswith('.'):  continue
        verify_only=True if dir.endswith(tuple(ignore['directories'])) else False
        cnt_check=cnt_tot=0
        if (verbosity > 0 and len(files) > 0): 
            print "\n\n************************************************"
            print "Now on directory %s" % dir 
            print "************************************************"
        for name in [x for x in files if not 
                     (   x.endswith(ignore['suffixes']) 
                      or x.endswith(tuple([y+".gz" for y in ignore['suffixes'] ])) 
                      or x.endswith(tuple([y.upper() for y in ignore['suffixes'] ])) 
                      or x.endswith(tuple([(y+".gz").upper() for y in ignore['suffixes'] ]))
                      or x.startswith('.')
                     ) ]:
            cnt_tot+=1
            one=os.path.join(dir, name)
            if (verbosity > 1): print "\nTIMESTAMP:  " + datetime.now().strftime("%Y-%m-%d %X")

            if logdir:
                logpath= os.path.join(logdir,os.path.relpath(dir,basedir))
                if not os.path.isdir(logpath):  os.makedirs(logpath)
                logfile=os.path.join(logpath,name+".check.log")
                if (verbosity > 1 and verify_only==False): print("CHECKING %s;  see log in %s" % (one, logfile) )
                elif (verbosity > 1 and verify_only==True): print("Verifying %s;  see log in %s" % (one, logfile) )
                sys.stdout.flush()
            else:
                logfile=sys.stdout
                if (verbosity > 1 and verify_only==False): print("CHECKING %s" % one)
                elif (verbosity > 1 and verify_only==True): print("Verifying %s" % one)
                sys.stdout.flush()
            #  Returns status that contains both the counts of errors,
            #  warnings, and the logged reports.  
            status=ogip_check(one,None,logfile,2,dtype=default_type,vonly=verify_only,meta_key=meta_key)

            #if status.status != 0:
                #print("ERROR:  failed to check file %s;  see log in %s\nContinuing." % (one, logfile) )
            if status.status == 0:
                if (verbosity > 1 and verify_only==False): 
                    print("Done.  Found file of type %s with %s errors and %s (level=2) and %s (level=3) warnings." % (status.otype, status.tot_errors(),status.tot_warnings(2),status.tot_warnings(3) ) )
                    cnt_check+=1
                elif (verbosity > 1 and verify_only==True): print("File is in an ignored directory, skipping OGIP standards check.")
                sys.stdout.flush()

            # Store the retstat info for the file
            summary.update(dir=dir,file=name,statobj=status)
            gc.collect() # Should be unnecessary but just in case.
        if (verbosity > 1 and len(files) > 0 and verify_only==False):  print("\n********\nFound %s files in this directory that could be checked out of %s that were examined and %s that were ignored (for %s total in the directory)." % (cnt_check,cnt_tot,len(files)-cnt_tot,len(files)) )


    print("\n***************************************************")
    print("Done checking.  Now to summarize:\n")
    print("The total number of files found: %s" % int(summary.count_bad()+summary.count_verified()+summary.count_checked()) )
    print("The total number of files that could not be opened as FITS:  %s" % summary.count_fopen() )
    print("The total number of files whose type could not be recognized:  %s" % summary.count_unrecognized() )
    print("The total number of files that failed FITS verify and could NOT be 'fixed':  %s" % summary.count_fver_bad() )
    print("The total number of files that failed FITS verify but 'fixed':  %s" % summary.count_fver_fixed() )
    print("The total number of files that could not be checked for other reasons:  %s" % int(summary.count_bad()-summary.count_fopen()-summary.count_unrecognized()-summary.count_fver_bad() ) )
    print("The total number of files verified only:  %s" % summary.count_verified() )
    print("The total number of files checked:  %s" % summary.count_checked() )
    print("The total number of files with no OGIP warnings or errors:  %s" % summary.count_good() )
    print("The total number of files with no errors but with OGIP level 3 warnings:  %s" % summary.count_warned(3) )
    print("The total number of files with no errors but with OGIP level 2 warnings:  %s" % summary.count_warned(2) )
    print("The total number of files with OGIP errors:  %s" % summary.count_failed() )

    print("")
    for k in sorted(summary.count_types):
        print("Checked %s files of type %s" % (summary.count_types[k],k) )

    print("")
    #  Summarize required keywords for each type:
    types=[ 'TIMING', 'SPECTRAL', 'RMF', 'ARF', 'CALDB', 'IMAGE' ]

    for t in sorted(types):
        print("")
        if t not in summary.count_types:
            #  Don't bother to summarize types for which no files were found
            print("Found no files of type %s" % t)
            continue 
        print("Summary of missing required keywords and columns for type %s:" % t)
        cnt=0
        dict=ogip_dictionary(t)
        if t == 'CALDB':
            #  CALDB types don't have required extnames.  Any files
            #  checked as CALDB types will store the extn as CALFILE.
            check_extns=['CALFILE']
        elif t == 'IMAGE':
            check_extns=['IMAGE']
        else:
            check_extns=dict['EXTENSIONS']['REQUIRED']+ dict['EXTENSIONS']['OPTIONAL']
        for extn in check_extns:
            if extn in summary.count_extnames[t]:
                for k in dict[extn]['KEYWORDS']: 
                    if dict[extn]['KEYWORDS'][k]['level']!=1:  continue
                    if summary.count_missing_key(t,extn,k) > 0:
                        cnt+=1
                        print("    Found %s (out of %s) files have at least one extension %s missing key %s." % (summary.count_missing_key(t,extn,k), summary.count_extnames[t][extn], extn, k) )
                for c in dict[extn]['COLUMNS']:
                    if dict[extn]['COLUMNS'][c]['level']!=1: continue
                    if summary.count_missing_col(t,extn,c) > 0:
                        cnt+=1
                        print("    Found %s (out of %s) files have at least one extension %s missing column %s." % (summary.count_missing_col(t,extn,c), summary.count_extnames[t][extn], extn, c) )
        if cnt==0:  print("     None of these are missing required keywords or columns.")

    if len(summary.unrec_extnames.keys()) > 0:
        print("\nFound the following unrecognized extensions (with total number of each):")
        for k in sorted(summary.unrec_extnames):
            print ("    %s (%s)" % (k,summary.unrec_extnames[k]) )
        print("")
    else:  print("\n(No unrecognized extensions.)")
                        
    print("\nDone\n")

    return




if __name__== "__main__":
    dir = "."

    status = ogip_check_dir(dir)

    exit(status.status)


