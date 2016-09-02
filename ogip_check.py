from __future__ import print_function
import astropy.io.fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *
import os.path

def ogip_check(input,otype,logfile,verbosity):
    """
    Checks for the existence of OGIP required keywords and columns 
    for FITS files based on the Standards doccumented here:  
    
    https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html

    Failure to open the file as a FITS file will result in non-zero retstat.status.

    Failure in the FITS verify step will result in non-zero retstat.status.

    Failure to actually compare the file to any dictionary will 
    result in a non-zero return value in the retstat.status attribute.  

    But errors in required keys or columns will simply be counted in
    the retstat.ERRORS attribute.

    """
    #
    # TODO - ADD OPTIONS FOR VERBOSITY

    filename=input
    status=retstat()

    #  Should be given either sys.stdout for the logfile, or a string
    #  filename to open:
    if isinstance(logfile,(str,unicode)):
        try:  logf=open(logfile,'w')
        except:  
            status.update(report="ERROR:  Cannot open output log file %s" % logfile, status=1)
            return status
    else:
        if logfile is not sys.stdout:
            status.update(report="ERROR:  Cannot write to log file %s" % logfile, status=1)
            return status
        else:
            logf=logfile


    #  Even just trying to open it can lead to pyfits barfing errors
    #  and warnings all over.  Leave stdout though, since
    #  robust_open() logs what happens to stdout and we'll want to see
    #  that.
    with stdouterr_redirector(logf,stdout=False):
        try:
            hdulist = robust_open(filename,logf,status)
        except IOError:
        #  Cases should be trapped in robust_open and already
        #  reflected in status:
            return status
        except:
        #  For the unexpected, e.g., the system call to gunzip fails
        #  for some reason:
            print("ERROR:  Non-IOError error raised.  Status is %s." % status.status)
            return status
        else:
        #  Just in case:
            if status.status != 0:
                print("ERROR:  No error raised, but status is %s." % status.status)
                return status


    #  Basic FITS verification:
    fits_errs=False
    if logf is not sys.stdout:
        #  Temporarily redirect STDOUT and STDERR for pyfits verification:
        with stdouterr_redirector(logf):
            try:
                hdulist.verify(option='exception')
            except pyfits.verify.VerifyError:
                #  Trap the error so that we can abort this check but
                #  not necessarily the whole process if running in
                #  batch.  (This way, finishes the redirection at the
                #  end of the with statement block.)
                fits_errs=True
        if fits_errs == True:
            status.update(report="ERROR:  file does not pass FITS verification.",fver=1,status=1)
            return status
    else:
        hdulist.verify(option='exception')


    numext= len(hdulist)
    if numext <= 1:
        status.update(report="ERROR: File needs at least 1 BINARY extension in addition to the PRIMARY; only found %i total" % numext, status=1)
        return status

    # Get a list of all the extnames (after the 0th, which is PRIMARY)
    # which are BINTABLE type in the file using a list comprehension.  
    # Obviously, this needs to change if we do images. 
    extnames= [x.name for x in hdulist[1:] if x.header['XTENSION'].startswith('BINTABLE') ]
    if len(extnames) == 0:
        status.update(report="ERROR:  file does not have BINTABLE extension.",status=1)
        return status

    if extnames[0] == '':
        #  Let these continue for now and see if HDUCLS
        status.update(report="WARNING:  file has BINTABLE extension with no name")

    #  Try to determine the type from the first (not PRIMARY) extension:
    if otype is None:
        for t in ['TIMING','SPECTRAL','RMF','ARF','CALDB']:

            #  Integral files sometimes start with indexing;  skip this
            if hdulist[1].header['EXTNAME']=='GROUPING': xno=2
            else: xno=1

            ref_extn=ogip_determine_ref(hdulist[xno], t)

            if ref_extn:
                otype = t
                print("\nChecking file as type %s" % otype,file=logf)
                break
        if otype is None:
            status.update(report="ERROR:  failed to determine the file type;  trying CALDB",err=1,log=logf)
            otype='CALDB'
        print("\n(If this is incorrect, rerun with --t and one of TIMING, SPECTRAL, CALDB, RMF, or ARF.\n",file=logf)

    else:
        print("\nChecking file as type %s" % otype,file=logf)

    status.otype=otype

    ogip_dict=ogip_dictionary(otype)
    if ogip_dict==0:
        status.update(report="ERROR:  do not recognize OGIP type %s" % otype, status=1)
        return status

    fname = filename
    if "/" in filename:
        fname=filename[filename.rfind("/")+1:]


    # List of required or optional extensions.  
    ereq=ogip_dict['EXTENSIONS']['REQUIRED']
    eopt=ogip_dict['EXTENSIONS']['OPTIONAL']

    check=True if otype == 'CALDB' else False #  No required extension name(?)

    # If there are multiple entries in the required set, only one must
    # be in the file to be tested for it to pass.  This code will have
    # to change if there is a requirement for multiple extensions.
    for ref in ereq:
        for actual in extnames:
            if ref in actual: check=True
            
    if not check:
        status.update(report="ERROR: %s does not have any of the required extension names" % fname, log=logf,err=1,extn='none')

    # We have the type, now simply loop over the extensions found in
    # the file and check whatever's there against what's expected for
    # the type, except for calibration files, which could have any
    # extension name.
    #
    # Note that the name in the dictionary may be a
    # substring of the name in the file (e.g., for RMF files, the
    # required extension is 'MATRIX' while the file may have 
    #  'SPECRESP MATRIX'.)   So check for substrings.

    extns_checked=0

    for this_extn in extnames:  
        
        #  Determines which reference extension to check this one
        #  against.  Sometimes not named correctly, but we'd still
        #  want to check.
        if otype == 'CALDB':
            ref_extn='CALFILE'
        else:
            ref_extn = ogip_determine_ref( hdulist[extnames.index(this_extn)+1], otype )

        if ref_extn:
            print("\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,ref_extn),file=logf)
            missing=cmp_keys_cols(hdulist,filename,this_extn,ref_extn,ogip_dict,logf,status)
            extns_checked+=1
        else:
            print("\nExtension '%s' is not an OGIP defined extension for this type;  ignoring.\n" % this_extn,file=logf)


    if extns_checked > 0:
        print("\n=============== %i Errors and %i Warnings Found in %s extensions checked ===============\n" %(status.tot_errors(), status.tot_warnings(),extns_checked),file=logf)
    else:
        status.update(report="\nERROR:  No extensions could be checked\n",log=logf,status=1)


    if status.tot_errors() > 0:
        ogip_fail(filename,ogip_dict,logf)
    else:
        print("\n===========================================================",file=logf)
        print("\nFile %s conforms to the OGIP Standards" % filename,file=logf)


    return status





if __name__== "__main__":
    filename = "test_files/CRAB_daily_lc.fits"

    status = ogip_check(filename)

    exit(status.status)

