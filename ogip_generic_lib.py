from __future__ import print_function
import astropy.io.fits as pyfits
import sys
from contextlib import contextmanager
import os
import subprocess


"""
Library of generic functions used by OGIP check utilities.
"""


#
#  Temporarily redirects stdout and stderr to an already-open output
#  log file.
#
@contextmanager
def stdouterr_redirector(stream):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

"""  Alternate way? 
class stdouterr_redirector2():
    def __init__(self, stream):
        self.stream = stream
    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.stream
        sys.stderr = self.stream
    def __exit__(self, type, value, traceback):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
"""


class statinfo:
    def __init__(self):
        self.REPORT=[]
        self.WARNINGS=0
        self.ERRORS=0
        self.MISKEYS=[]
        self.MISCOLS=[]

class retstat:
    """

    For passing status information through module functions and back
    to calling codes without global variables.  

    REPORT contains the logged reports to print
    WARNINGS counts the number of warning messages (i.e. RECOMMENDED properties that fail)
    ERRORS counts the number of error messages (i.e. REQUIRED properties that fail)
    status counts running errors such as missing files, unrecognized formats, etc.

    """
    def update(self, extn=None, report=None, miskey=None, miscol=None, status=0, warn=0,err=0,log=sys.stdout,otype=None):
        #  Set an error status for the file if nonzero
        self.status+=status
        #  Set the file type
        if otype:  self.otype=otype
        #  Print the report for this update
        print(report,file=log)

        #  If an extension is not given, nothing else to do, since the
        #  above are the only two attributes that apply to the file as
        #  a whole.  (Note that the report isn't saved in this case.)
        if not extn:
            return

        #  Create the entry for the extension name if it doesn't already exist
        if extn not in self.extns:
            self.extns[extn]=statinfo()

        if report:  self.extns[extn].REPORT.append(report)
        if miskey:  self.extns[extn].MISKEYS.append(miskey)
        if miscol:  self.extns[extn].MISCOLS.append(miscol)

        self.extns[extn].WARNINGS+=warn
        self.extns[extn].ERRORS+=err


    def __init__(self,otype='unknown'):
        self.status=0
        self.otype=otype
        self.extns={}

    def tot_errors(self):
        errs=0
        for extn in self.extns.itervalues():
            errs+= extn.ERRORS
        return errs

    def tot_warnings(self):
        warns=0
        for extn in self.extns.itervalues():
            warns+= extn.WARNINGS
        return warns





def robust_open(filename,status):

    tmpname=''

    try:
        hdulist=pyfits.open(filename)

    except IOError:

        if filename.endswith(".gz"):
            #  For files named ".gz" that aren't really gzipped, FITS
            #  tools fall over quite naturally.  So create a link
            #  without the ".gz" and try to open it through that.
            tmpname='./.ogip_check_tmp_'+os.path.basename(filename)[:-3]
            if os.path.islink(tmpname):
                os.remove(tmpname)
            os.symlink(filename,tmpname)
            try:
                hdulist=pyfits.open(tmpname)
                    
            except IOError:
                os.remove(tmpname)
                status.update(report="ERROR: Could not open %s as a FITS file (gzipped or not); RETURNING" % os.path.basename(filename), status=1)
                raise IOError
        
            else:
                print("WARNING:  filename %s ends with .gz but appears not to be gzipped." % os.path.basename(filename))

        elif filename.endswith(".Z"):
            tmpname='./.ogip_check_tmp_'+os.path.basename(filename)
            #status.update(report="ERROR: cannot currently open zipped files; RETURNING", status=1)
            #raise IOError
            subprocess.call("cp %s %s" % (filename,tmpname),shell=True)
            subprocess.call("gunzip %s" % tmpname,shell=True)
            tmpname=tmpname[:-2]
            try:
                hdulist=pyfits.open(tmpname)
            except IOError:
                os.remove(tmpname)
                status.update(report="ERROR: Could not open %s as a FITS file (even unzipped); RETURNING" % os.path.basename(filename), status=1)
                raise IOError
            except:
                status.update(report="ERROR:  cannot unzip file %s" % os.path.basename(filename),status=1)
                os.remove(tmpname)
            else:
                os.remove(tmpname)

        else:
            status.update(report="ERROR: could not open %s as a FITS file; RETURNING" % filename, status=1)
            raise IOError

    except:
        print("DEBUGGING:  how did I get here?")


    if os.path.islink(tmpname):  os.unlink(tmpname)

    return hdulist




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

    hdr = hdu[extno].header

    colnames = hdu[extno].data.names
    colnames = [x.upper().strip() for x in colnames] # convert to uppercase, remove whitespace

    missing_keywords = []
    missing_columns = []
    extna=ref_extn.upper().strip()

    ogip=ogip_dict[extna]

    for key in ogip['KEYWORDS']['REQUIRED']:
        Foundkey = check_keys(key, hdr,logf,status)
        if not Foundkey:
            status.update(extn=extna,report="ERROR: Key %s not found in %s[%s]" % (key,file, this_extn), err=1,log=logf,miskey=key)

    for key in ogip['KEYWORDS']['RECOMMENDED']:
        Foundkey = check_keys(key,hdr,logf,status)
        if not Foundkey:
            status.update(extn=extna,report="WARNING: Key %s not found in %s[%s]" % (key,file, this_extn), warn=1,log=logf)

    for col in ogip['COLUMNS']['REQUIRED']:
        Foundcol = check_cols(col, colnames,logf,this_extn,status)
        if not Foundcol:
            status.update(extn=extna,report="ERROR: Required column %s missing from %s[%s]" % (col, file,  this_extn), err=1,log=logf, miscol=col)

    for col in ogip['COLUMNS']['RECOMMENDED']:
        Foundcol = check_cols(col, colnames,logf,this_extn,status)
        if not Foundcol:
            status.update(extn=extna,report= "WARNING: Recommended column %s missing from %s[%s]" % (col, file,  this_extn), warn=1,log=logf, miscol=col)

    # Backward compatibility
    missing={'REF_EXTN':ref_extn ,'MISSING_KEYWORDS':status.extns[extna].MISKEYS, 'MISSING_COLUMNS':status.extns[extna].MISCOLS}

    return missing



def key_hasvalue(key, header,logf, status):
    """
    checks if a keyword with a specific value exists in the file header
    key should be of the form
    key = 'HDUCLASS[OGIP]'
    where the value in the square brackets is the allowed value of the keyword
    This assumes a given keyword can have only 1 allowed value
    header is a fits header as returned from pyfits
    Returns True if the keyword is found with the correct value, False otherwise
    @param key:
    @param header:
    @return:
    """


    beg=key.find("[")
    val=key[beg+1:key.find(']')].strip().upper()
    k=key[0:beg]
    Match = False
    if k in header:
        if type(header[k]) is str:
            aval=header[k].strip().upper()
            if aval == val:
                Match = True
        elif type(header[k]) is int:
            aval=header[k]
            if aval==int(val):
                Match = True
        if Match==False:
            status.update(extn=header['EXTNAME'],report="Keyword %s Found, but Value = %s, should be %s" % (k, aval, val),log=logf, warn=1)

    else:
        status.update(extn=header['EXTNAME'], report="Keyword %s not found in header" % k, log=logf)

    return Match



def check_altkey(key, header,logf,status):
    """
    Check for presence of alternate key names
    @param key:
    @param header:
    @return:
    """


    altkeys = key.split('|')
    altkeys = [x.upper().strip() for x in altkeys]
    count = 0
    Foundkey = False
    while (count < len(altkeys)) and not Foundkey:
        akey = altkeys[count]
        if "+" in akey:  # check for coupled keywords
            Foundkey = check_groupkey(akey, header, logf, status)
        else:  # does not contain a + sign
            Foundkey = akey in header.keys()  # true if akey in hdr
        count += 1
    if count == len(altkeys) and not Foundkey:
        rpt = "Alternate keywords %s not found in header" % key
        print(rpt,file=logf)
    return Foundkey


def check_altcols(col, colnames,logf,status):
    """

    @param col:
    @param colnames:
    @return:
    """


    altcols = col.split('|')
    altcols = [x.upper().strip() for x in altcols]
    count = 0
    Foundcol = False
    while (count < len(altcols)) and not Foundcol:
        acol = altcols[count]
        Foundcol = acol in colnames  # true if acol in colnames
        count += 1
    if count == len(altcols) and not Foundcol:
        rpt = "Alternate Column %s not found in header" % col
        print(rpt,file=logf)
    else:
        print("Alternate Column %s found in header" % acol,file=logf)
    return Foundcol



def check_groupkey(key, header, logf, status):
    """
    this function checks for grouped keywords of the form MJDREFI+MJDREFF, in which case both keywords need
    to exist in the header; True if so, False otherwise
    A more general case is a group like key =  A[a]+B[b]+C[c] where A, B & C all need to be present
    and they all need to have the specified values a, b, c respectively; True if so, False otherwise
    @param key:
    @param header:
    @return:
    """

    groupkeys = key.split('+')
    groupkeys = [x.upper().strip() for x in groupkeys]
    hkeys = header.keys()
    hkeys = [x.upper().strip() for x in hkeys]
    Foundkey = False
    Foundkey = set(groupkeys) < set(header.keys())  # true if groupkeys a subset of header keywords
    if not Foundkey:
        rpt = "Group keywords %s not Found in Header" % key
        print(rpt,file=logf)
    else: # all keywords exist in header; do they have the correct value, if specified?
        for k in groupkeys:
            if "[" in k: # value is specified
                Foundkey = key_hasvalue(k, header,logf, status)
    return Foundkey



def check_enumkey(key, header,logf,status):
    """
    this function checks for enumerated keywords of the form EMIN*, which will return
    all header keywords beginning with EMIN
    @param key:
    @param header:
    @return:
    """

    Foundkey = True
    val=header[key]
    if len(val) == 0: # search did not return any elements
        rpt = "Enumerated keywords %s not Found in Header" % key
        print(rpt,file=logf)
        Foundkey = False
    return Foundkey



def check_groupcols(col, colnames, extn, status):
    """
    this function checks for grouped keywords of the form MJDREFI+MJDREFF, in which case both keywords need
    to exist in the header; True if so, False otherwise
    A more general case is a group like key =  A[a]+B[b]+C[c] where A, B & C all need to be present
    and they all need to have the specified values a, b, c respectively; True if so, False otherwise
    @param key:
    @param header:
    @return:
    """
    groupcols = col.split('+')
    groupcols = [x.upper().strip() for x in groupcols]
    colnames = [x.upper().strip() for x in colnames]
    Foundcol = False
    Foundcol = set(groupcols) < set(colnames)  # true if groupcolss a subset of column names
    if not Foundcol:
        status.update(extn=extn,report="Group columns %s not Found in Table" % col, log=logf)
    else: # all columns are defined
        print("Group columns %s found in Table",file=logf)
    return Foundcol



def check_keys(key, header,logf,status):
    """
    checks that the key appears in the header
    @param key:
    @param header:
    @return:
    """


    if "|" in key:  # this means that the keyword has an alternative definition (like MJDREF, MJDREFF+MJDREFI)
        Foundkey = check_altkey(key, header,logf,status)
    elif "[" in key:  # this means this keyword has an allowed value, which is bracketed by [ and ]
        Foundkey = key_hasvalue(key, header,logf,status)
    elif "+" in key:  # this is a group keyword with no alternates
        Foundkey = check_groupkey(key, header,logf,status)
    elif "*" in key: # this is an enumerated keyword (EMIN1...EMINn for example
        Foundkey = check_enumkey(key, header,logf,status)
    else:
        Foundkey = key in header.keys()
    return Foundkey



def check_cols(col, colnames,logf, extn, status):
    """
    checks that the col appears in the list of column names
    @param col:
    @param header:
    @return:
    """


    Foundcol = True
    if "|" in col:  # this means that the column has an alternative definition (like COUNTS|RATE)
        Foundcol = check_altcols(col, colnames,logf,status)
    elif "+" in col:  # group column; all columns must be present if one column is
        Foundcol = check_groupcols(col, colnames, extn, status)
    else:
        Foundcol = col in colnames
    return Foundcol




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
