import pyfits
from ogip_dictionary import ogip_dictionary

status = 0
REPORT = ['FILE CONFORMS TO THE OGIP CONVENTIONS']
WARNINGS=0
ERRORS=0

def cmp_keys_cols(filename, extname):
    """
    for a given hdu from a fits extension, get the required and optional keywords and columns
    then check that the given hdu has all the required elements

    filename is the name of the file that needs to be checked
    extname should be either RATE, EVENTS, GTI or ENEBAND

    @param hdu:
    @param type:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

    file = filename[filename.rfind('/')+1:] # remove directory path

    ogip_dict = ogip_dictionary('timing')

    hdu = pyfits.open(filename)
    extlist = [x.name for x in hdu]
    try:
        extno = extlist.index(extname)
    except ValueError:
        print "Extension Name %s not found in file %s" % (extname, filename)
        return

    print "Checking Extension # %i EXTNAME = %s" % (extno, extname)
    hdr = hdu[extno].header

    colnames = hdu[extno].data.names
    colnames = [x.upper().strip() for x in colnames] # convert to uppercase, remove whitespace

    missing_keywords = ['']
    missing_columns = ['']
    extna=extname.upper().strip()

    ogip=ogip_dict[extna]

    for key in ogip['KEYWORDS']['REQUIRED']:
        Foundkey = check_keys(key, hdr)
        if not Foundkey:
            rpt= "ERROR: Key %s not found in %s[%s]" % (key,file, extname)
            missing_keywords.append(key)
            print rpt
            REPORT.append(rpt)
            ERRORS += 1
    for key in ogip['KEYWORDS']['RECOMMENDED']:
        Foundkey = check_keys(key,hdr)
        if not Foundkey:
            rpt= "WARNING: Key %s not found in %s[%s]" % (key,file,extname)
            print rpt
            REPORT.append(rpt)
            WARNINGS += 1
    for col in ogip['COLUMNS']['REQUIRED']:
        Foundcol = check_cols(col, colnames)
        if not Foundcol:
            rpt = "ERROR: Required column %s missing from %s[%s]" % (col, file, extname)
            print rpt
            REPORT.append(rpt)
            ERRORS += 1
            missing_columns.append(col)
    for col in ogip['COLUMNS']['RECOMMENDED']:
        Foundcol = check_cols(col, colnames)
        if not Foundcol:
            rpt = "WARNING: Recommended column %s missing from %s[%s]" % (col, file, extname)
            print rpt
            REPORT.append(rpt)
            WARNINGS += 1
    if len(missing_keywords) > 1:
        missing_keywords= missing_keywords[1:]
    if len(missing_columns) > 1:
        missing_columns= missing_columns[1:]

    missing={'EXTNAME':extname ,'MISSING_KEYWORDS':missing_keywords, 'MISSING_COLUMNS':missing_columns}

    return missing


def key_hasvalue(key, header):
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
    global ERRORS, WARNINGS
    global REPORT

    beg=key.find("[")
    val=key[beg+1:key.find(']')]
    k=key[0:beg]
    Found = False
    if k in header:
        if header[k].strip().upper() == val:
            Found = True
        else:
            rpt = "Keyword %s Found, but Value = %s, should be %s" % (k, header[k].upper().strip(), val.upper().strip())
            print rpt
            REPORT.append(rpt)
            WARNINGS += 1
    else:
        rpt = "Keyword %s not found in header" % k
        print rpt
        REPORT.append(rpt)
    return Found

def check_altkey(key, header):
    """
    Check for presence of alternate key names
    @param key:
    @param header:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

    altkeys = key.split('|')
    altkeys = [x.upper().strip() for x in altkeys]
    count = 0
    Foundkey = False
    while (count < len(altkeys)) and not Foundkey:
        akey = altkeys[count]
        if "+" in akey:  # check for coupled keywords
            Foundkey = check_groupkey(akey, header)
        else:  # does not contain a + sign
            Foundkey = akey in header.keys()  # true if akey in hdr
        count += 1
    if count == len(altkeys) and not Foundkey:
        rpt = "Alternate keywords %s not found in header" % key
        print rpt
    return Foundkey

def check_altcols(col, colnames):
    """

    @param col:
    @param colnames:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

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
        print rpt
    else:
        print "Alternate Column %s found in header" % acol
    return Foundcol


def check_groupkey(key, header):
    """
    this function checks for grouped keywords of the form MJDREFI+MJDREFF, in which case both keywords need
    to exist in the header; True if so, False otherwise
    A more general case is a group like key =  A[a]+B[b]+C[c] where A, B & C all need to be present
    and they all need to have the specified values a, b, c respectively; True if so, False otherwise
    @param key:
    @param header:
    @return:
    """
    global ERRORS, WARNINGS
    global REPORT

    groupkeys = key.split('+')
    groupkeys = [x.upper().strip() for x in groupkeys]
    hkeys = header.keys()
    hkeys = [x.upper().strip() for x in hkeys]
    Foundkey = False
    Foundkey = set(groupkeys) < set(header.keys())  # true if groupkeys a subset of header keywords
    if not Foundkey:
        rpt = "Group keywords %s not Found in Header" % key
        print rpt
    else: # all keywords exist in header; do they have the correct value, if specified?
        for k in groupkeys:
            if "[" in k: # value is specified
                Foundkey = key_hasvalue(k, header)
    return Foundkey

def check_enumkey(key, header):
    """
    this function checks for enumerated keywords of the form EMIN*, which will return
    all header keywords beginning with EMIN
    @param key:
    @param header:
    @return:
    """
    global ERRORS, WARNINGS
    global REPORT

    Foundkey = True
    val=header[key]
    if len(val) == 0: # search did not return any elements
        rpt = "Enumerated keywords %s not Found in Header" % key
        print rpt
        Foundkey = False
    return Foundkey

def check_groupcols(col, colnames):
    """
    this function checks for grouped keywords of the form MJDREFI+MJDREFF, in which case both keywords need
    to exist in the header; True if so, False otherwise
    A more general case is a group like key =  A[a]+B[b]+C[c] where A, B & C all need to be present
    and they all need to have the specified values a, b, c respectively; True if so, False otherwise
    @param key:
    @param header:
    @return:
    """
    global ERRORS, WARNINGS
    global REPORT

    groupcols = col.split('+')
    groupcols = [x.upper().strip() for x in groupcols]
    colnames = [x.upper().strip() for x in colnames]
    Foundcol = False
    Foundcol = set(groupcols) < set(colnames)  # true if groupcolss a subset of column names
    if not Foundcol:
        rpt = "Group columns %s not Found in Table" % col
        print rpt
        REPORT.append(rpt)
    else: # all columns are defined
        print "Group columns %s found in Table"
    return Foundcol

def check_keys(key, header):
    """
    checks that the key appears in the header
    @param key:
    @param header:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

    if "|" in key:  # this means that the keyword has an alternative definition (like MJDREF, MJDREFF+MJDREFI)
        Foundkey = check_altkey(key, header)
    elif "[" in key:  # this means this keyword has an allowed value, which is bracketed by [ and ]
        Foundkey = key_hasvalue(key, header)
    elif "+" in key:  # this is a group keyword with no alternates
        Foundkey = check_groupkey(key, header)
    elif "*" in key: # this is an enumerated keyword (EMIN1...EMINn for example
        Foundkey = check_enumkey(key, header)
    else:
        Foundkey = key in header.keys()
    return Foundkey

def check_cols(col, colnames):
    """
    checks that the col appears in the list of column names
    @param col:
    @param header:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

    Foundcol = True
    if "|" in col:  # this means that the column has an alternative definition (like COUNTS|RATE)
        Foundcol = check_altcols(col, colnames)
    elif "+" in col:  # group column; all columns must be present if one column is
        Foundcol = check_groupcols(col, colnames)
    else:
        Foundcol = col in colnames
    return Foundcol




def ogip_fail(filename):
    """
    Prints failure report for ogip_timing_check
    @param filename:
    @return:
    """

    global ERRORS, WARNINGS
    global REPORT

    print "\n===========================================================\n"
    print "FAILURE: %s is not a Valid OGIP formatted file" % filename
    print "Please see OGIP/93-003: The Proposed Timing FITS File Format for High Energy Astrophysics Data"
    print "Available at"
    print "   http://heasarc.gsfc.nasa.gov/FTP/caldb/docs/ogip/fits_formats/docs/rates/ogip_93_003/ogip_93_003.pdf"
    return

def ogip_timing_check(filename):
    """
    checks for the existence of OGIP required keywords for timing files based on
    http://heasarc.gsfc.nasa.gov/FTP/caldb/docs/ogip/fits_formats/docs/rates/ogip_93_003/ogip_93_003.pdf
    """
    #import pyfits

    global ERRORS, WARNINGS
    global REPORT

    print "\nChecking file %s" % filename
    fname = filename
    if "/" in filename:
        fname=filename[filename.rfind("/")+1:]

    try:
        hdulist= pyfits.open(filename)
    except:
        print "ERROR: Could not open %s; RETURNING" % filename
        ERRORS += 1
        return
    hdulist.verify()
    numext= len(hdulist)
    if numext < 1:
        rpt= "ERROR: Timing File needs at least 1 extension, found %i" % numext
        print rpt
        REPORT.append(rpt)
        ERRORS += 1
        ogip_fail(filename)
    # Get a list of all the extnames in the file using a list comprehension
    extname= [x.name for x in hdulist]
    # Find extension HEADER with EXTNAME= RATE or EVENTS
    if 'RATE' in extname:
        print "\n=============== Checking RATE Extension ===============\n"
        missing = cmp_keys_cols(filename, 'RATE')
    elif 'EVENTS' in extname:
        print "\n=============== Checking EVENTS Extension ===============\n"
        missing = cmp_keys_cols(filename, 'EVENTS')
    else:
        rpt= "ERROR: %s has no RATE or EVENTS extension" % fname
        print rpt
        REPORT.append(rpt)
        rpt= "%s NOT A VALID OGIP TIMING FILE \n" % filename
        print rpt
        print "QUITTING"
        REPORT.append(rpt)
        ERRORS +=  1
        REPORT = REPORT[1:]
        return status, REPORT
    print "\n=============== Checking GTI Extension ==============="
    if 'GTI' in extname:
        missing = cmp_keys_cols(filename, 'GTI')
    else:
        print "\nFile %s does not contain a GTI extension\n" % fname
    print "\n=============== Checking TIMEREF Extension ==============="
    if 'TIMEREF' in extname:
        missing = cmp_keys_cols(filename,'TIMEREF')
    else:
        print "\nFile %s does not contain a TIMEREF extension" % fname
    print "\n=============== Checking ENEBAND Extension ==============="
    if 'ENEBAND' in extname:
        missing = cmp_keys_cols(filename,'ENEBAND')
    else:
        print "\nFile %s does not contain a ENEBAND extension" % fname
    REPORT = REPORT[1:]
    if ERRORS > 0:
        ogip_fail(filename)
    else:
        print "\n==========================================================="
        print "\nFile %s conforms to the OGIP Standards" % filename

    if len(REPORT)>1:
        REPORT=REPORT[1:]
    print "\n=============== %i Errors and %i Warnings Found ===============\n" %(ERRORS, WARNINGS)
    return REPORT

if __name__== "__main__":
    filename= "/Users/corcoran/program/HEASARC/missions/Fermi/Data_Products/gbm_occultation_light_curves/201507/CRAB_daily_lc_mfc.fits"
    #filename="/Users/corcoran/research/ETA_CAR/Swift/2014/work/00091911036/sw00091911036xwtw2stsr.lc"
    #filename = "/Users/corcoran/Downloads/xh95702010201_s0a.lc"
    #filename = "/Users/corcoran/research/ETA_CAR/Swift/2014/quicklook/work/00091911045/xspec/ec_src.pha"
    #filename = "/Users/corcoran/research/ETA_CAR/CHANDRA2/repro/seqid/200057/632/acisf00632_evt1a.fits"

    REPORT = ogip_timing_check(filename)

    #print "\nStatus= %i" % status
    #print "\nPrinting Report"
    #for i in REPORT:
    #    print i
    #missing=cmp_keys_cols(filename,'RATE')
    # print missing
    #stat=check_ogip_rate_extension(filename,1)