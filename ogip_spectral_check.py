import pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *


def ogip_spectral_check(filename):
    """
    checks for the existence of OGIP required keywords for spectral files based on
    OGIP/92-007 The OGIP Spectral File Format at 
    https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/summary/ogip_92_007_summary.html
    """
    #import pyfits
    # TODO - ADD OPTIONS FOR VERBOSITY, LOGFILE

    ogip_dict=ogip_dictionary('SPECTRAL')
    status=retstat(0,['FILE CONFORMS TO THE OGIP CONVENTIONS'],0,0)

    print "\nChecking file %s as type SPECTRAL" % filename
    fname = filename
    if "/" in filename:
        fname=filename[filename.rfind("/")+1:]

    try:
        hdulist= pyfits.open(filename)
    except:
        print "ERROR: Could not open %s; RETURNING" % filename
        status.ERRORS += 1
        return
    hdulist.verify()
    numext= len(hdulist)
    if numext < 1:
        rpt= "ERROR: Timing File needs at least 1 extension, found %i" % numext
        print rpt
        status.REPORT.append(rpt)
        status.ERRORS += 1
        ogip_fail(filename)
    # Get a list of all the extnames in the file using a list comprehension
    extname= [x.name for x in hdulist]
    # Find extension HEADER with EXTNAME= RATE or EVENTS
    if 'SPECTRUM' in extname:
        print "\n=============== Checking RATE Extension ===============\n"
        missing = cmp_keys_cols(filename, 'SPECTRUM',ogip_dict, status)
    else:
        rpt= "ERROR: %s has no SPECTRUM extension" % fname
        print rpt
        status.REPORT.append(rpt)
        rpt= "%s NOT A VALID OGIP SPECTRAL FILE \n" % filename
        print rpt
        print "QUITTING"
        status.REPORT.append(rpt)
        status.ERRORS +=  1
        status.REPORT = status.REPORT[1:]
        return status.status, status.REPORT
    print "\n=============== Checking GTI Extension ==============="
    if 'GTI' in extname:
        missing = cmp_keys_cols(filename, 'GTI',ogip_dict, status)
    else:
        print "\nFile %s does not contain a GTI extension\n" % fname
    print "\n=============== Checking DETECTOR Extension ==============="
    if 'DETECTOR' in extname:
        missing = cmp_keys_cols(filename,'DETECTOR',ogip_dict,status)
    else:
        print "\nFile %s does not contain a DETECTOR extension" % fname
    print "\n=============== Checking HISTORY Extension ==============="
    if 'HISTORY' in extname:
        missing = cmp_keys_cols(filename,'HISTORY',ogip_dict,status)
    else:
        print "\nFile %s does not contain a HISTORY extension" % fname
    status.REPORT = status.REPORT[1:]
    if status.ERRORS > 0:
        ogip_fail(filename,ogip_dict)
    else:
        print "\n==========================================================="
        print "\nFile %s conforms to the OGIP Standards" % filename

    if len(status.REPORT)>1:
        status.REPORT=status.REPORT[1:]
    print "\n=============== %i Errors and %i Warnings Found ===============\n" %(status.ERRORS, status.WARNINGS)
    return status.REPORT

if __name__== "__main__":
    filename = "~/space/work/heasarc/ogip/xh91127030412_b0.pha"

    REPORT = ogip_spectral_check(filename)

