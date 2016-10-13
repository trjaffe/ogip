from __future__ import print_function
import astropy.io.fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *
import os.path

def ogip_check(input,otype,logfile,verbosity,dtype=None):
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
    #  and warnings all over (which we catch in the specific log, and
    #  just don't want to stderr at this point).  Leave stdout though,
    #  since robust_open() logs what happens to stdout and we'll want
    #  to see that.
    if logf is not sys.stdout:
        with stdouterr_redirector(logf,redir_out=False):
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
                sys.stdout.flush()
                return status
            else:
            #  Just in case:
                if status.status != 0:
                    print("ERROR:  No error raised, but status is %s." % status.status)
                    sys.stdout.flush()
                    return status
    else:
        try:
            hdulist = robust_open(filename,logf,status)
        except IOError:
        #  Cases should be trapped in robust_open and already
        #  reflected in status:
            return status
        except:
        #  For the unexpected, e.g., the system call to gunzip fails
        #  for some reason:
            print("ERROR:  Non-IOError error raised.  Error is %s, status is %s." % (sys.exc_info()[0],status.status) )
            sys.stdout.flush()
            return status
        else:
        #  Just in case:
            if status.status != 0:
                print("ERROR:  No error raised, but status is %s." % status.status)
                sys.stdout.flush()
                return status



    #  Basic FITS verification:
    fits_errs=ogip_fits_verify(hdulist,filename,logf,status)
    if fits_errs == 1:
        status.update(report="ERROR:  file does not pass FITS verification but able to continue.",fver=1)
    if fits_errs == 2:  
        status.update(report="ERROR:  file does not pass FITS verification;  giving up.",fver=2,status=1)
        return status


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
        #  Integral files sometimes start with indexing;  skip this
        xno=1
        if 'EXTNAME' in hdulist[1].header:
            if hdulist[1].header['EXTNAME']=='GROUPING': xno=2
            if xno+1 > len(hdulist):
                status.update(report="ERROR:  File has only GROUPING extension.", status=1)
                return status

        ref_extn, otype =ogip_determine_ref(hdulist[xno])

        if ref_extn is not None and otype is not None:
            if 'EXTNAME' in hdulist[xno].header:
                print("\nChecking file as type %s (match for this file's %s and reference extension %s)" % (otype,hdulist[xno].header['EXTNAME'],ref_extn),file=logf)
            else:
                print("\nChecking file as type %s (match for this file's NAMELESS and reference extension %s)" % (otype,ref_extn),file=logf)
        elif otype is None:
            if dtype:
                if dtype == 'none':
                    status.update(report="ERROR:  do not recognize the file as any type (extnames "+", ".join(extnames)+")",status=1,unrec=1)
                    return status
                else:
                    status.update(report="ERROR:  failed to determine the file type;  trying %s" % dtype,err=1,log=logf)
                    otype=dtype
            else:
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
            #  The type is already set.  Throw away it's return val here.
            ref_extn, t = ogip_determine_ref( hdulist[extnames.index(this_extn)+1], otype )

        if ref_extn:
            print("\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,ref_extn),file=logf)
            cmp_keys_cols(hdulist,filename,this_extn,ref_extn,ogip_dict,logf,status)
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

