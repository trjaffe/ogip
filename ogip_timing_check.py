from astropy.io import fits as pyfits
from ogip_dictionary import ogip_dictionary
from ogip_generic_lib import *


def ogip_timing_check(filename):
    """
    checks for the existence of OGIP required keywords for timing files based on
    http://heasarc.gsfc.nasa.gov/FTP/caldb/docs/ogip/fits_formats/docs/rates/ogip_93_003/ogip_93_003.pdf

    changes: MFC 20160811 added ogip_dict to call to cmp_keys_cols
    """
    #
    # TODO - ADD OPTIONS FOR VERBOSITY, LOGFILE

    ogip_dict=ogip_dictionary('TIMING')
    status=retstat(0,['FILE CONFORMS TO THE OGIP CONVENTIONS'],0,0)

    print "\nChecking file %s as type TIMING" % filename
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
    if 'RATE' in extname:
        print "\n=============== Checking RATE Extension ===============\n"
        missing = cmp_keys_cols(filename, 'RATE',ogip_dict, status)
    elif 'EVENTS' in extname:
        print "\n=============== Checking EVENTS Extension ===============\n"
        missing = cmp_keys_cols(filename, 'EVENTS', ogip_dict, status)
    else:
        rpt= "ERROR: %s has no RATE or EVENTS extension" % fname
        print rpt
        status.REPORT.append(rpt)
        rpt= "%s NOT A VALID OGIP TIMING FILE \n" % filename
        print rpt
        print "QUITTING"
        status.REPORT.append(rpt)
        status.ERRORS +=  1
        status.REPORT = status.REPORT[1:]
        return status.status, status.REPORT
    print "\n=============== Checking GTI Extension ==============="
    if 'GTI' in extname:
        missing = cmp_keys_cols(filename, 'GTI', ogip_dict, status)
    else:
        print "\nFile %s does not contain a GTI extension\n" % fname
    print "\n=============== Checking TIMEREF Extension ==============="
    if 'TIMEREF' in extname:
        missing = cmp_keys_cols(filename,'TIMEREF',ogip_dict, status)
    else:
        print "\nFile %s does not contain a TIMEREF extension" % fname
    print "\n=============== Checking ENEBAND Extension ==============="
    if 'ENEBAND' in extname:
        missing = cmp_keys_cols(filename,'ENEBAND',ogip_dict,status)
    else:
        print "\nFile %s does not contain a ENEBAND extension" % fname
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
    #filename= "/Users/corcoran/program/HEASARC/missions/Fermi/Data_Products/gbm_occultation_light_curves/201507/CRAB_daily_lc_mfc.fits"
    #filename="/Users/corcoran/research/ETA_CAR/Swift/2014/work/00091911036/sw00091911036xwtw2stsr.lc"
    #filename = "/Users/corcoran/Downloads/xh95702010201_s0a.lc"
    #filename = "/Users/corcoran/research/ETA_CAR/Swift/2014/quicklook/work/00091911045/xspec/ec_src.pha"
    #filename = "/Users/corcoran/research/ETA_CAR/CHANDRA2/repro/seqid/200057/632/acisf00632_evt1a.fits"
    #filename="http://heasarc.gsfc.nasa.gov/FTP/rosat/data/pspc/processed_data/200000/rp200069n00/rp200069n00_ltc.fits.Z"
    #filename = "/Users/mcorcora/Downloads/rp200069n00_ltc.fits"
    filename = "test_files/CRAB_daily_lc.fits"

    REPORT = ogip_timing_check(filename)

    #print "\nStatus= %i" % status
    #print "\nPrinting Report"
    #for i in REPORT:
    #    print i
    #missing=cmp_keys_cols(filename,'RATE')
    # print missing
    #stat=check_ogip_rate_extension(filename,1)
