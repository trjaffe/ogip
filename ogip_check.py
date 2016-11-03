from __future__ import print_function
import astropy.io.fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *
import os.path

def ogip_check(input,otype,logfile,verbosity,dtype=None,vonly=False):
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

    try:
        logf=init_log(logfile,status)
    except:
        return status

 

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
        status.update(report="ERROR:  file %s does not pass FITS verification but able to continue." % filename,fver=1,verbosity=verbosity)
    if fits_errs == 2:  
        status.update(report="ERROR:  file %s does not pass FITS verification;  giving up." % filename,fver=2,status=1,verbosity=verbosity)
        return status
    if vonly:  
        status.update(vonly=True)
        return status

    #  Determine the file type from extensions, keywords, or the
    #  default type. 
    if otype is None:
        otype=ogip_determine_ref_type(filename, hdulist,status,logf,dtype,verbosity)
        if otype is None:
            return status
        status.otype=otype
    else:
        print("\nChecking file as type %s" % otype,file=logf)

    ogip_dict=ogip_dictionary(otype)
    if ogip_dict==0:
        status.update(report="ERROR:  do not recognize OGIP type %s" % otype, status=1,verbosity=verbosity)
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
    extnames= [x.name for x in hdulist[1:]]
    for ref in ereq:
        for actual in extnames:
            if ref in actual: check=True
            
    if not check and not otype=='IMAGE':
        status.update(report="ERROR: %s does not have any of the required extension names" % fname, log=logf,level=1,extn='none',verbosity=verbosity)

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


    if otype=='IMAGE' and hdulist[0].header['NAXIS']!=0:
        #  There's a primary image to check, but cannot assume it's the only one!
        extnames.insert(0,'PRIMARY')

    for this_extn in extnames:  
        
        #  Determines which reference extension to check this one
        #  against.  Sometimes not named correctly, but we'd still
        #  want to check.
        if otype == 'CALDB':
            ref_extn='CALFILE'
        elif this_extn=='PRIMARY':
            ref_extn='IMAGE'
        else:
            ref_extn, t = ogip_determine_ref_extn( hdulist[extnames.index(this_extn)+1], otype )

        if ref_extn:
            print("\n=============== Checking '%s' extension against '%s' standard ===============\n" % (this_extn,ref_extn),file=logf)
            cmp_keys_cols(hdulist,filename,this_extn,ref_extn,ogip_dict,logf,status)
            extns_checked+=1
        else:
            status.update(report="Extension '%s' is not an OGIP defined extension for this type;  ignoring.\n" % this_extn,log=logf,unrec_extn=this_extn,verbosity=verbosity)


    if extns_checked > 0:
        print("\n=============== %i Errors and %i Warnings Found in %s extensions checked ===============\n" %(status.tot_errors(), status.tot_warnings(),extns_checked),file=logf)
    else:
        status.update(report="\nERROR:  No extensions could be checked\n",log=logf,status=1,verbosity=verbosity)


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

