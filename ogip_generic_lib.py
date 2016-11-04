from __future__ import print_function
import astropy.io.fits as pyfits
import sys
import os
import subprocess
from ogip_dictionary import ogip_dictionary
import re
import gc

"""
Library of generic functions used by OGIP check utilities.
"""


#
#  Temporarily redirects stdout and stderr to an already-open output
#  log file.
#
"""  Alternate way?  Move import to hea

from contextlib import contextmanager

@contextmanager
def stdouterr_redirector(stream,redir_out=True,redir_err=True):
    if redir_out: 
        old_stdout = sys.stdout
        sys.stdout = stream
    if redir_err: 
        old_stderr = sys.stderr
        sys.stderr = stream
    try:
        yield
    finally:
        if redir_out:  sys.stdout = old_stdout
        if redir_err:  sys.stderr = old_stderr
"""

class stdouterr_redirector():
    def __init__(self, stream=None,redir_out=True,redir_err=True):
        if stream is not None:
            self.stream = stream
        else:
            self.stream=open(os.devnull,"w")
        self.redir_out=redir_out
        self.redir_err=redir_err
        self.reverse=False
    def __enter__(self):
        if self.stream is not sys.stdout:
            self.reverse=True
            if self.redir_out:
                self.old_stdout = sys.stdout
                sys.stdout = self.stream
            if self.redir_err:
                self.old_stderr = sys.stderr
                sys.stderr = self.stream
    def __exit__(self, type, value, traceback):
        if self.reverse:
            if self.redir_out:
                sys.stdout = self.old_stdout
            if self.redir_err:
                sys.stderr = self.old_stderr
  
class statinfo:
    """

    Status information stored for each extension

    REPORT contains the logged reports to print
    LEVELS counts the number of warning messages for each level, 0 to 3
    status counts running errors such as missing files, unrecognized formats, etc.


    """
    def __init__(self):
        self.REPORT=[]
        self.WARNINGS={0:0,1:0,2:0,3:0}
        self.MISKEYS=[]
        self.MISCOLS=[]





class retstat:
    """

    For passing status information through module functions and back
    to calling codes without global variables.  

    """
    def update(self, extn=None, report=None, miskey=None, miscol=None, status=0, level=0,log=sys.stdout,otype=None,fver=0,fopen=0,unrec=0,verbosity=2,unrec_extn=None,vonly=False):
        #  Set an error status for the file if nonzero;  this will halt the checks.
        self.status+=status
        #  Flag problems opening the file as FITS specifically
        self.fopen+=fopen
        #  Flag unrecognized FITS files
        self.unrec+=unrec
        #  Flag FITS verification errors specifically
        self.fver+=fver
        #  Flag whether OGIP checks were performed or only FITS verification:
        self.vonly=vonly
        #  Set the file type
        if otype:  self.otype=otype
        #  Print the report for this update
        if (verbosity > 1):  print(report,file=log)
        if vonly: return

        if unrec_extn is not None:  
            self.unrec_extns.append(unrec_extn)
            return

        #  Just in case
        if not extn:
            extn="none"

        #  Create the entry for the extension name (an object of
        #  statinfo type) if it doesn't already exist
        if extn not in self.extns:
            self.extns[extn]=statinfo()

        if report:  self.extns[extn].REPORT.append(report)
        if miskey:  self.extns[extn].MISKEYS.append(miskey)
        if miscol:  self.extns[extn].MISCOLS.append(miscol)

        self.extns[extn].WARNINGS[level]+=1



    def __init__(self,otype='unknown'):
        self.status=0
        self.fver=0
        self.fopen=0
        self.unrec=0
        self.vonly=False
        self.otype=otype
        self.extns={}
        self.unrec_extns=[]

    def tot_errors(self):
        errs=0
        for extn in self.extns.itervalues():
            errs+= extn.WARNINGS[1]
        return errs

    def tot_warnings(self):
        warns=0
        for extn in self.extns.itervalues():
            warns+=extn.WARNINGS[3]+extn.WARNINGS[2]
        return warns




def robust_open(filename,logf,status):

    tmpname=''

    try:
        print("Attempting to open file %s" % filename,file=logf)
        hdulist=pyfits.open(filename,mmap=True)

    except IOError:
        if filename.endswith(".gz"):
            #  For files named ".gz" that aren't really gzipped, FITS
            #  tools fall over quite naturally.  So create a link
            #  without the ".gz" and try to open it through that.
            print("Failed to open as a FITS file.  Since it's named .gz, try after removing suffix.",file=logf)
            tmpname='./.ogip_check_tmp_'+os.path.basename(filename)[:-3]
            if os.path.islink(tmpname):  os.remove(tmpname)
            os.symlink(filename,tmpname)
            try:
                hdulist=pyfits.open(tmpname,mmap=True)
            except IOError:
                os.remove(tmpname)
                status.update(report="ERROR: Could not open %s as a FITS file (gzipped or not); RETURNING" % os.path.basename(filename), status=1,fopen=1)
                raise IOError
            else:
                print("WARNING:  Filename %s ends with .gz but appears not to be gzipped;  has been opened after removing the suffix." % os.path.basename(filename))
        
        elif filename.endswith(".Z"):
            print("Failed to open as a FITS file.  Trying to unzip first.",file=logf)
            tmpname='./.ogip_check_tmp_'+os.path.basename(filename)
            #status.update(report="ERROR: cannot currently open zipped files; RETURNING", status=1)
            #raise IOError
            if subprocess.call("cp %s %s" % (filename,tmpname),shell=True):
                print("Failed to copy locally!",file=logf)
                raise IOError
            try:
                print("Trying to gunzip it.",file=logf)
                if subprocess.call("gunzip %s" % tmpname,shell=True):
                    print("gunzip command itself failed!",file=logf)
                    raise IOError
            except:
                if os.path.isfile(tmpname):  os.remove(tmpname)
                status.update(report="ERROR:  cannot unzip file %s" % os.path.basename(filename),status=1)
                raise
            else: 
                try:
                    print("Trying now to open it again as FITS.",file=logf)
                    tmpname=tmpname[:-2]
                    hdulist=pyfits.open(tmpname,mmap=True)
                except:
                    os.remove(tmpname)
                    print("Still cannot open it, quitting.",file=logf)
                    status.update(report="ERROR: Could not open %s as a FITS file (after unzipped); RETURNING" % os.path.basename(filename), status=1,fopen=1)
                    raise IOError

        else:

            status.update(report="ERROR: could not open %s as a FITS file; RETURNING" % filename, status=1,fopen=1)
            raise IOError


    except:
        print("DEBUGGING:  how did I get here?")

    #  Success should always end up here:
    if os.path.islink(tmpname):  os.unlink(tmpname)
    if os.path.isfile(tmpname):  os.remove(tmpname)

    print("File opened successfully.",file=logf)

    return hdulist








def cleanup(hdulist):
    for hdu in hdulist:
        del hdu.data
    hdulist.close()
    gc.collect()








def ogip_fits_verify(hdulist,filename,logf,status):

    """

    #  Temporarily redirect STDOUT and STDERR for pyfits verification:
    with stdouterr_redirector(logf):
        try:
            #  Trap the error so that we can abort this check but
            #  not necessarily the whole process if running in
            #  batch.  (This way, finishes the redirection at the
            #  end of the with statement block.)
            hdulist.verify(option='exception')
        except pyfits.verify.VerifyError:
            #  Run it again with option='warn', since annoyingly,
            #  fits.verify(option='exception') does not print any
            #  information on why it failed!  And option='warn'
            #  would make it hard to trap the outcome.
            hdulist.verify(option='warn')
            fits_err=2

    return fits_err

    """

    fits_err=0

    print("Running basic FITS verification with external call to ftverify.",file=logf)

    try:
        ftv=subprocess.Popen("ftverify %s" % filename,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
        out, err = ftv.communicate()
        stat=ftv.returncode
        if stat != 0: raise OSError
    except OSError:
        print("ERROR: external call to ftverify returns an error.")
#        exit(-1)

    #  I don't actually want to keep the STDOUT from ftverify, only
    #  STDERR that lists the errors.
    result=err.split('\n')
    if result != ['']:
        [status.update(report="Ftverify:  %s" % x,log=logf) for x in result]
        fits_errs=1

        #  See if we can continue.  Use
        #  astropy.io.fits.verify(option='fix').  If it can, it fixes
        #  the copy in memory.  If not, it throws an exception.  This
        #  function will return 2 if this happens.  Otherwise, we try
        #  to continue despite the possible issues (return value 1).
        #  Presume that if the verify() is satisfied, then we won't
        #  run into exceptions later.

        with stdouterr_redirector(logf):
            try:
                print("Trying to fix simple errors with astropy.io.fits.verify(option='fix')",file=logf)
                hdulist.verify(option='fix')
            except:
                fits_errs=2

    else:
        #  Even if ftverify finds nothing, check the Python version
        #  just in case.  

        with stdouterr_redirector(logf):
            try:
                print("Nothing from ftverify, trying with astropy.io.fits.verify(option='exception')",file=logf)
                hdulist.verify(option='exception')
            except:
                #  Not yet had a case get into this block.  
                print("WARNING:  errors found by astropy.io.fits.verify() apparently not found by ftverify",file=logf)
                fits_errs=1
                #  Then try to fix it, which will thrown an exception if it cannot:
                try: 
                    print("Trying to fix simple errors with astropy.io.fits.verify(option='fix')",file=logf)
                    hdulist.verify(option='fix')
                except:
                    print("Unsuccessful, giving up",file=logf)
                    fits_errs=2
            else:
                fits_errs=0

    return fits_errs




#  Try to determine the type from the PRIMARY or first extension:
#
def ogip_determine_ref_type(filename,hdulist,status,logf,dtype=None,verbosity=3):

    #  Easy if there's nothing but a primary extension; that has to be
    #  an image.  (But that's not the only extension that can be an
    #  imaging extension!)
    if len(hdulist) == 1:
        if hdulist[0].header['NAXIS']==0:
            status.update(report="ERROR:  PRIMARY extension has NAXIS==0 but there are no further extensions.", status=1,verbosity=verbosity)
            return None
        else:
            print("Found a file with only a PRIMARY extension.  Testing as an IMAGE.", file=logf)
            return 'IMAGE'
    #  Second easiest case:  if there's an image in the PRIMARY or first extension, then it's an IMAGE type.  
    elif hdulist[0].header['NAXIS']!=0:
        print("Found a file with an image in the PRIMARY extension.  Testing as an IMAGE.", file=logf)
        return 'IMAGE'
    elif 'XTENSION' in hdulist[1].header and 'IMAGE' in hdulist[1].header['XTENSION']:
        if hdulist[1].header['XTENSION']!='IMAGE':  status.update(report="ERROR:  Extension has XTNAME=%s, which should be 'IMAGE'." % hdulist[1].header['XTENSION'],level=1,extn='IMAGE',log=logf,verbosity=verbosity)
        print("Found a file with an IMAGE extension.  Testing as an IMAGE.", file=logf)
        return 'IMAGE'

    types=['TIMING','SPECTRAL','RMF','ARF','CALDB','IMAGE']
    # Get a list of all the extnames (after the 0th, which is PRIMARY)
    extnames= [x.name for x in hdulist[1:]]
    if extnames[0] == '':
        #  Let these continue for now and see if HDUCLS
        status.update(report="WARNING:  file has an extension with no name",verbosity=verbosity,extn='',level=2)

    #  Integral files sometimes start with indexing;  skip this
    xno=1
    if 'EXTNAME' in hdulist[1].header:
        if hdulist[1].header['EXTNAME']=='GROUPING': xno=2
        if xno+1 > len(hdulist):
            status.update(report="WARNING:  File has only GROUPING extension.", status=1,verbosity=verbosity)
            return None

    ref_extn, otype =ogip_determine_ref_extn(hdulist[xno])

    if ref_extn is not None:
        if 'EXTNAME' in hdulist[xno].header:
            print("\nChecking file as type %s (match for this file's %s and reference extension %s)" % (otype,hdulist[xno].header['EXTNAME'],ref_extn),file=logf)
        else:
            print("\nChecking file as type %s (match for this file's NAMELESS and reference extension %s)" % (otype,ref_extn),file=logf)
    else:
        if dtype:
            if dtype == 'none':
                status.update(report="WARNING:  do not recognize the file %s" % filename+" as any type (extnames "+", ".join(extnames)+")",status=1,unrec=1,verbosity=verbosity)
                status.extns=extnames
                return None
            else:
                status.update(report="ERROR:  failed to determine the file type;  trying %s" % dtype,level=1,log=logf,verbosity=verbosity)
                otype=dtype
        else:
            status.update(report="ERROR:  failed to determine the file type;  trying CALDB",level=1,log=logf,verbosity=verbosity)
            otype='CALDB'
    print("\n(If this is incorrect, rerun with --t and one of TIMING, SPECTRAL, CALDB, RMF, or ARF.\n",file=logf)
    return otype




#  Given an extension in a real file, see if there's a match in a
#  given dictionary.  If no type is given, it checks them all to find
#  the right one, otherwise checks only the extensions of the
#  specified type.  It will
#  - check the EXTNAME against the dict['EXTENSIONS']
#  - check the EXTNAME against the dict['ALT_EXTNS'] (which requires a loop over these)
#  - check the HDUCLAS1 and HDUCLAS2 keywords against those for each dict['EXTENSIONS']
#  and return the first matching reference extension, or None.
#
def ogip_determine_ref_extn(in_extn,intype=None):
    if intype is not None:
        types=[intype]
    else:
        types=['TIMING','SPECTRAL','RMF','ARF','CALDB']

    #  Look for a matching extension based on the EXTNAME or its HDUCLAS* keywords.  
    #
    #  Since a GTI extension can be found in a spectral, timing, or
    #  image file, cannot use it to determine the type.  (And this
    #  function will be called within ogip_determine_ref_type().)
    #
    #  Likewise, HDUCLAS1==RESPONSE can be either RMF or ARF or
    #  possibly CALDB, so check HDUCLAS2.

    if 'XTENSION' not in in_extn.header:
        #  Only PRIMARY doesn't have this
        return 'IMAGE','IMAGE'
    elif in_extn.header['XTENSION'] == 'IMAGE':
        return 'IMAGE', 'IMAGE'
    elif in_extn.header['XTENSION'] == 'BINTABLE':
        #  Object needed for eval() 
        h=hdr_check(in_extn.header,in_extn.columns) 
    else:
        return None, None
        

    #  First, check the extensions.  
    for otype in types:
        ogip_dict=ogip_dictionary(otype)
        all_extns=ogip_dict['EXTENSIONS']['REQUIRED']+ogip_dict['EXTENSIONS']['OPTIONAL']

        #  Easy case: the extension name matches the reference
        #  extension name for a type
        if 'EXTNAME' in in_extn.header:

            if in_extn.header['EXTNAME'] in all_extns:  
                return in_extn.header['EXTNAME'], otype

            #  Second easiest case: for each reference extension, 
            #  see if the ref extname is a substring of the
            #  actual extension name (e.g., RMF type 'MATRIX'
            #  extension is sometimes 'SPECRESP MATRIX' in some
            #  missions:
            for extn in all_extns:
                if ( extn in in_extn.header['EXTNAME'] and extn != ''):
                    return extn, otype

            #  If that hasn't worked, check alternate extension
            #  names for each defined extension:
            for extn in [x for x in all_extns if x in ogip_dict['ALT_EXTNS'] ] :
                for aextn in ogip_dict['ALT_EXTNS'][extn]:
                    if aextn in  in_extn.header['EXTNAME']:
                        return extn, otype

    #  If that didn't find a match, then compare the required HDUCLAS1
    #  and HDUCLAS2 keywords.

    #  Check more-specific HDUCLAS2 first. Both ARF and RMF may have
    #  HDUCLAS1==RESPONSE, so they'd all end up whichever came
    #  first if you check that first. Check HDUCLAS2 first, which
    #  is MATRIX versus SPECRESP. 
    #
    #  Note that if it's there, it's in REQUIRED.  Not there for CALDB type.
    #
    #  Note also that the HDUCLAS2 requirement sometimes checks
    #  HDUCLAS3 as well, and it might fail because of HDUCLAS3 being
    #  incorrect.  If so, it might still then match when HDUCLAS1 is
    #  checked.  
    #
    for otype in types:
        ogip_dict=ogip_dictionary(otype)
        all_extns=ogip_dict['EXTENSIONS']['REQUIRED']+ogip_dict['EXTENSIONS']['OPTIONAL']

        for extn in all_extns:

            if 'HDUCLAS2' in in_extn.header and 'HDUCLAS2' in ogip_dict[extn]['KEYWORDS']:
                if eval(ogip_dict[extn]['KEYWORDS']['HDUCLAS2']["req"]):
                    return extn, otype

            #  Check less-specific HDUCLAS1, but not for ARF or RMF,
            #  because both have value RESPONSE. 
            if 'HDUCLAS1' in in_extn.header and 'HDUCLAS1' in ogip_dict[extn]['KEYWORDS']:
                if eval(ogip_dict[extn]['KEYWORDS']['HDUCLAS1']["req"]):
                    return extn, otype

    #  Lastly, since there's no other way to recognize a CALDB type:
    if (intype is None and 'CCLS0001' in in_extn.header) or intype=='CALDB':
        return 'CALFILE', 'CALDB'

    #  If you get here, no match, return Nones
    return None, None




def cmp_keys_cols(hdu, filename, this_extn, ref_extn, ogip_dict, logf, status):
    """
    for a given filename from a fits file, get the required and optional keywords and columns
    then check that the given hdu has all the required elements

    filename is the name of the file that needs to be checked
    ref_extn should be either RATE, EVENTS, GTI or ENEBAND

    @param filename: name of file being checked
    @param this_extn:  name of the extension being checked
    @param ref_extn: name of reference extension (not always the same)
    @param ogip_dict: ogip_dictionary to check against
    @param status: return status
    @return:
    """
    file = filename[filename.rfind('/')+1:] # remove directory path

    extlist = [x.name for x in hdu]
        
    extno=extlist.index(this_extn)  

    missing_keywords = []
    extna=ref_extn.upper().strip()

    ogip=ogip_dict[extna]

    #  The hdr_check() object that holds the header as well as the
    #  functions in which the requirements are encoded.
    if ref_extn=='IMAGE':
        h=hdr_check(hdu[extno].header,None)
    else:
        h=hdr_check(hdu[extno].header,hdu[extno].columns) 

    #  Each req is a string containing code that can be evaluated that
    #  uses the methods of the hdr_check() object that must be called
    #  h and whatever logic is needed to express the requirement.
    #  
    #  Check mandatory keyword requirements.   (Sort by decending level and then alphabetically.)
    print("Checking keywords:\n")
    for key,req in sorted(ogip['KEYWORDS'].iteritems(), key=lambda(k,v): (v['level'], k)):
        if not eval(req["req"]):  
            if req["level"] == 1:  status.update(extn=extna,report="ERROR: Key %s incorrect in %s[%s]" % (key,file, this_extn), level=req["level"],log=logf,miskey=key)
            else:  status.update(extn=extna,report="WARNING%s: Key %s incorrect in %s[%s]" % (req["level"],key,file, this_extn), level=req["level"],log=logf)

    if ref_extn=='IMAGE':
        return


    #  DO NOT USE THIS!  For large files in memory, this somehow
    #  causes memory usage to climb to several times the size of the
    #  file.  No idea why.  Just accessing the data attribute of the
    #  file that's gunzipped in memory?  Whatever.  Don't use the
    #  .data
    #  
    #colnames = hdu[extno].data.names
    #colnames = [x.upper().strip() for x in colnames] # convert to uppercase, remove whitespace
    colnames=[hdu[extno].header[key].upper().strip() for key in hdu[extno].header if 'TTYPE' in key]
    missing_columns = []

    print("\nChecking columns:\n")
    for col,req in sorted(ogip['COLUMNS'].iteritems(),key=lambda(k,v):(v['level'],k)):
        if not eval(req['req']):
            if req["level"] == 1:  status.update(extn=extna,report="ERROR: column %s incorrect in %s[%s]" % (col, file,  this_extn), level=req["level"],log=logf, miscol=col)
            else:  status.update(extn=extna,report="WARNING%s: column %s incorrect in %s[%s]" % (req["level"],col, file,  this_extn), level=req["level"],log=logf)

    return





"""

The class object that holds a header (a dictionary of key-value
pairs) and has methods for checking the existence and value of
individual keys.


For checking whether a requirement is satisfied by a given header.  Can
simply be the existence of a single key.  Can also be arbitrarily
complicated combination of tests.  The requirement must be written
assuming an instance h of the hdr_check() class which contains methods 

h.Exists('KEYNAME'):   returns boolean;  accepts 'KEY*" for partial matches.
h.hasVal('KEYNAME','VALUE'):  returns boolean for integer or string == comparison
h.intVal('KEYNAME'):  returns the value of the keyword cast as int()
h.strVal("KEYNAME'):  returns the value of the keyword cast as str()

For example, a requirement may be given as a string such as:

req="h.Exists('KEY1') or ( h.Exists('KEY2') and h.hasVal('KEY3','VAL3') )"

and that string will be called with eval() and returned.  
""" 
class hdr_check():
    def __init__(self,hdr,columns):
        self.hdr=hdr
        #  Columns is a astropy.io.fits ColDefs type
        if columns is not None:  self.columns=[c.upper().strip() for c in columns.names]

    #  Check function that checks for existence of a given keyword,
    #  and if a value is given, checks that it has that value.
    #  Returns boolean.
    def Exists(self,key):
        #  Check keys with wildcard first
        if "*" in key:
            return len(self.hdr[key]) > 0
        #  Otherwise, just check if the key exists
        else: return key in self.hdr


    def hasVal(self,k,val,part=False):  
        # checks if a keyword with a specific value exists in the file
        #  header.  If part==Trueq, checks for the reference val to be
        #  a substring of the actual keyword.
        Match = False
        if k in self.hdr:
            if type(self.hdr[k]) is str:
                aval=self.hdr[k].strip().upper()
                if (part==False and aval == val) or (part==True and val in aval):
                    Match = True
            elif type(self.hdr[k]) is int:
                aval=self.hdr[k]
                if aval==int(val):
                    Match = True
            elif type(self.hdr[k]) is bool:
                aval=self.hdr[k]
                if aval==bool(val):
                    Match = True
            else:
                print("ERROR:  Check your requirements definition.  Cannot do exact comparison with anything except string, bool, and integer types.")
                exit(1)
        return Match

    def intVal(self,key):
        if key in self.hdr:
            return int(self.hdr[key])
        else:
            return None

    def strVal(self,key):
        if key in self.hdr:
            return str(self.hdr[key])
        else:
            return ''

    def hasCol(self,col,part=False):
        if self.columns is None:  return False
        if part:
            for c in self.columns:
                if col in c:  return True
        else:
            return col in self.columns
         


def ogip_fail(filename,ogip_dict,logf):
    """
    Prints failure report for ogip_check
    @param filename:
    @return:
    """


    print("\n===========================================================\n",file=logf)
    print("FAILURE: %s is not a Valid OGIP formatted file" % filename,file=logf)
    print("Please see %s: %s" % (ogip_dict["REFERENCE"],ogip_dict["REFTITLE"]),file=logf)
    print("Available at",file=logf)
    print("   %s" % ogip_dict["REFURL"],file=logf)
    return







def init_log(logfile,status):
   #  Should be given either sys.stdout for the logfile, or a string
    #  filename to open:
    if isinstance(logfile,(str,unicode)):
        try:  logf=open(logfile,'w')
        except:  
            status.update(report="ERROR:  Cannot open output log file %s" % logfile, status=1,verbosity=verbosity)
            raise
    else:
        if logfile is not sys.stdout:
            status.update(report="ERROR:  Cannot write to log file %s" % logfile, status=1,verbosity=verbosity)
            raise
        else:
            logf=logfile

    return logf
