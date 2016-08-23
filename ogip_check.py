from __future__ import print_function
from astropy.io import fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *
import os.path

def ogip_check(input,type,logfile,verbosity):
    """

    Checks for the existence of OGIP required keywords and columns 
    for FITS files based on the Standards doccumented here:  
    
    https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html

    Any generic FITS-standard errors will also cause an exception.

    """
    #
    # TODO - ADD OPTIONS FOR VERBOSITY, LOGFILE

    filename=input
    status=retstat()

    #  Should be given either sys.stdout for the logfile, or a string
    #  filename to open:
    if isinstance(logfile,(str,unicode)):
        try:  logf=open(logfile,'w')
        except:  
            print("ERROR:  Cannot open output log file %",logfile)
            status.status+=1
            return status
    else:
        if logfile is not sys.stdout:
            print("ERROR:  Cannot write to log file %",logfile)
            status.status+=1
            return status
        else:
            logf=logfile


    try:
        hdulist= pyfits.open(filename)
    except:
        print("ERROR: Could not open %s as a FITS file; RETURNING" % filename)
        #  If the file exists but is not a FITS file, do not return an
        #  error status.  
        if not os.path.isfile(filename):
            # Only return an error status if you were given an input file
            #  that does not exist. Otherwise, may be called from
            #  ogip_check_dir, which will try to check everything,
            #  since there's no way to know if it's a FITS file or not
            #  just from the name.
            status.status += 1  
        return status

    hdulist.verify()
    numext= len(hdulist)
    if numext < 1:
        rpt= "ERROR: File needs at least 1 extension, found %i" % numext
        print(rpt,file=logf)
        status.REPORT.append(rpt)
        status.status += 1
        ogip_fail(filename)
        return status

    # Get a list of all the extnames in the file using a list comprehension
    extnames= [x.name for x in hdulist]
    if 'PRIMARY' in extnames:
        extnames.remove('PRIMARY')

    if type==None:
        #  Try to determine the type based on the name of the first
        #  extension.  Try CALDB if nothing else matches.
        if extnames[0] in ['RATE','EVENTS']: type='TIMING'
        elif extnames[0] == 'SPECTRUM': type='SPECTRAL'
        elif 'MATRIX' in extnames[0] or extnames[0]=='EBOUNDS': type='RMF'
        elif extnames[0]=='SPECRESP': type='ARF'
        else: type='CALDB'
        print("\nChecking file %s as type %s" % (filename,type),file=logf)
        print("\n(If this is incorrect, rerun with --t and one of TIMING, SPECTRAL, CALDB, RMF, or ARF.\n",file=logf)
    else:
        type=type
        print("\nChecking file %s as type %s" % (filename,type),file=logf)

    ogip_dict=ogip_dictionary(type)
    if ogip_dict==0:
        print("\nERROR:  do not recognize OGIP type %s" % type)
        status.status+=1
        return status

    fname = filename
    if "/" in filename:
        fname=filename[filename.rfind("/")+1:]


    # List of required or optional extensions.  
    ereq=ogip_dict['EXTENSIONS']['REQUIRED']
    eopt=ogip_dict['EXTENSIONS']['OPTIONAL']

    check=True if type == 'CALDB' else False #  No required extension name(?)

    # If there are multiple entries in the required set, only one must
    # be in the file to be tested for it to pass.  This code will have
    # to change if there is a requirement for multiple extensions.
    for x in ereq:
        for y in extnames:
            if x in y: check=True
    if not check:
        rpt= "ERROR: %s does not have any of the required extensions" % fname
        print(rpt,file=logf)
        status.REPORT.append(rpt)
        rpt= "%s NOT A VALID OGIP %s FILE \n" % (filename,type)
        print(rpt,file=logf)
        print("QUITTING",file=logf)
        status.REPORT.append(rpt)
        status.ERRORS +=  1
        status.status +=  1
        status.REPORT = status.REPORT[1:]
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
        if type=='CALDB':
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

    if status.ERRORS > 0:
        ogip_fail(filename,ogip_dict,logf)
    else:
        print("\n===========================================================",file=logf)
        print("\nFile %s conforms to the OGIP Standards" % filename,file=logf)

    print("\n=============== %i Errors and %i Warnings Found ===============\n" %(status.ERRORS, status.WARNINGS),file=logf)
    return status











if __name__== "__main__":
    filename = "test_files/CRAB_daily_lc.fits"

    status = ogip_check(filename)

    exit(status.status)

