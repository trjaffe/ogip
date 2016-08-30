from __future__ import print_function
import pyfits
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
    result in a non-zero return value in the retstat.status attribue.  
    But errors in required keys or columns will not;  they will 
    simply be counted in the retstat.ERRORS attribue.  

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


    #  Why doesn't this seem to trap correctly?
    try:
        hdulist = robust_open(filename,status)
    except IOError:
        #  Cases should be trapped in robust_open and already
        #  reflected in status:
        return status
    except:
        #  For the unexpected:
        print("ERROR:  Non-IOError error raised.  Status is %s." % status.status)
        return status
    else:
        #  Just in case:
        if status.status != 0:
            print("ERROR:  No error raised, but status is %s." % status.status)
            return status
        #else:
            #print("File opened successfully")


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
            status.update(report="ERROR:  file does not pass FITS verification;  aborting checks.",status=1)
            return status
    else:
        hdulist.verify(option='exception')


    numext= len(hdulist)
    if numext <= 1:
        status.update(report="ERROR: File needs at least 1 BINARY (not primary) extension, found %i total" % numext, status=1)
        return status

    # Get a list of all the extnames in the file using a list comprehension
    extnames= [x.name for x in hdulist]
    if 'PRIMARY' in extnames:
        extnames.remove('PRIMARY')

    if otype==None:
        #  Try to determine the type based on the name of the first
        #  extension.  Try CALDB if nothing else matches.
        if extnames[0] in ['RATE','EVENTS']: otype='TIMING'
        elif extnames[0] == 'SPECTRUM': otype='SPECTRAL'
        elif 'MATRIX' in extnames[0] or extnames[0]=='EBOUNDS': otype='RMF'
        elif extnames[0]=='SPECRESP': otype='ARF'
        else: otype='CALDB'
        print("\nChecking file %s as type %s" % (filename,otype),file=logf)
        print("\n(If this is incorrect, rerun with --t and one of TIMING, SPECTRAL, CALDB, RMF, or ARF.\n",file=logf)
    else:
        print("\nChecking file %s as type %s" % (filename,otype),file=logf)

    status.otype=otype

    ogip_dict=ogip_dictionary(otype)
    if ogip_dict==0:
        status.update(report="\nERROR:  do not recognize OGIP type %s" % otype, status=1)
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
    for x in ereq:
        for y in extnames:
            if x in y: check=True
    if not check:
        status.update(report="ERROR: %s does not have any of the required extensions" % fname, log=logf)
        status.update(report="%s NOT A VALID OGIP %s FILE \nQUITTING\n" % (filename,otype), log=logf,status=1,err=1)
        return status

    # We have the type, have checked that at least one of the required extensions is
    # there, and now simply loop over the extensions found in the file and check
    # whatever's there against what's expected for the type, except
    # for calibration files, which could have any extension name.

    # Note that the name in the dictionary may be a
    # substring of the name in the file (e.g., for RMF files, the
    # required extension is 'MATRIX' while the file may have 
    #  'SPECRESP MATRIX'.) So check for substrings.

    for this_extn in extnames:  

        #  Check any extensions found:
        if otype=='CALDB':
            print("\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,'CALFILE'),file=logf)
            missing=cmp_keys_cols(filename,this_extn,'CALFILE',ogip_dict, logf,status)

        #  Check only extensions recognized, i.e., defined in the
        #  dictionary, allowing partial matches:
        else:
            checked=False
            for ref_extn in ereq+eopt:
                if ref_extn in this_extn:
                    print("\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,ref_extn),file=logf)
                    missing=cmp_keys_cols(filename,this_extn,ref_extn,ogip_dict,logf,status)
                    checked=True
                    break
            if checked==False:
                print("\nExtension '%s' is not an OGIP defined extension for this type;  ignoring.\n" % this_extn,file=logf)

    if status.tot_errors() > 0:
        ogip_fail(filename,ogip_dict,logf)
    else:
        print("\n===========================================================",file=logf)
        print("\nFile %s conforms to the OGIP Standards" % filename,file=logf)

    print("\n=============== %i Errors and %i Warnings Found ===============\n" %(status.tot_errors(), status.tot_warnings()),file=logf)
    return status





if __name__== "__main__":
    filename = "test_files/CRAB_daily_lc.fits"

    status = ogip_check(filename)

    exit(status.status)

