from astropy.io import fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *


def ogip_check(args):
    """
    checks for the existence of OGIP required keywords for FITS files based on
    
    https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html

    """
    #
    # TODO - ADD OPTIONS FOR VERBOSITY, LOGFILE

    filename=args.input

    try:
        hdulist= pyfits.open(filename)
    except:
        print "ERROR: Could not open %s; RETURNING" % filename
        status.ERRORS += 1
        return
    hdulist.verify()
    numext= len(hdulist)
    if numext < 1:
        rpt= "ERROR: File needs at least 1 extension, found %i" % numext
        print rpt
        status.REPORT.append(rpt)
        status.ERRORS += 1
        ogip_fail(filename)

    # Get a list of all the extnames in the file using a list comprehension
    extnames= [x.name for x in hdulist]
    if 'PRIMARY' in extnames:
        extnames.remove('PRIMARY')

    if args.type==None:
        #  Try to determine the type based on the name of the first
        #  extension.  Try CALDB if nothing else matches.
        if extnames[0] in ['RATE','EVENTS']: type='TIMING'
        elif extnames[0] == 'SPECTRUM': type='SPECTRAL'
        elif 'MATRIX' in extnames[0] or extnames[0]=='EBOUNDS': type='RMF'
        elif extnames[0]=='SPECRESP': type='ARF'
        else: type='CALDB'
        print "\nChecking file %s as type %s" % (filename,type)
        print "\n(If this is incorrect, rerun with --t and one of TIMING, SPECTRAL, CALDB, RMF, or ARF.\n"
    else:
        type=args.type
        print "\nChecking file %s as type %s" % (filename,type)

    ogip_dict=ogip_dictionary(type)
    if ogip_dict==0:
        print "\nERROR:  do not recognize OGIP type %s" % type
        exit(1)

    status=retstat(0,['FILE CONFORMS TO THE OGIP CONVENTIONS'],0,0)

    fname = filename
    if "/" in filename:
        fname=filename[filename.rfind("/")+1:]


    # List of required or optional extensions.  
    ereq=ogip_dict['EXTENSIONS']['REQUIRED']
    eopt=ogip_dict['EXTENSIONS']['OPTIONAL']

    check=False if type != 'CALDB' else True #  No required extension name(?)

    # If there are multiple entries in the required set, only one must
    # be in the file to be tested for it to pass.  This code will have
    # to change if there is a requirement for multiple extensions.
    for x in ereq:
        for y in extnames:
            if x in y: check=True
    if not check:
        rpt= "ERROR: %s does not have any of the required extensions" % fname
        print rpt
        status.REPORT.append(rpt)
        rpt= "%s NOT A VALID OGIP %s FILE \n" % (filename,type)
        print rpt
        print "QUITTING"
        status.REPORT.append(rpt)
        status.ERRORS +=  1
        status.REPORT = status.REPORT[1:]
        return status

    # We have the type, have checked that at least one of the required extensions is
    # there, and now simply loop over the extensions and check
    # whatever's there. Note that the name in the dictionary may be a
    # substring of the name in the file (e.g., for RMF files, the
    # required extension is 'MATRIX' while the file may have 
    #  'SPECRESP MATRIX'.) So check for substrings.
    for this_extn in extnames:  
        if type=='CALDB':
            print "\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,'CALFILE')
            missing=cmp_keys_cols(filename,this_extn,'CALFILE',ogip_dict,status)
        else:
            checked=False
            for ref_extn in ereq+eopt:
                if ref_extn in this_extn:
                    print "\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,ref_extn)
                    missing=cmp_keys_cols(filename,this_extn,ref_extn,ogip_dict,status)
                    checked=True
            if checked==False:
                print "\nExtension '%s' is not an OGIP defined extension for this type;  ignoring.\n" % this_extn

    status.REPORT = status.REPORT[1:]
    if status.ERRORS > 0:
        ogip_fail(filename,ogip_dict)
    else:
        print "\n==========================================================="
        print "\nFile %s conforms to the OGIP Standards" % filename

    if len(status.REPORT)>1:
        status.REPORT=status.REPORT[1:]
    print "\n=============== %i Errors and %i Warnings Found ===============\n" %(status.ERRORS, status.WARNINGS)
    return status


if __name__== "__main__":
    filename = "test_files/CRAB_daily_lc.fits"

    status = ogip_timing_check(filename)

    exit(status.status)

