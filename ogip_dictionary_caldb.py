def ogip_dictionary_caldb():
    """

    For a given OGIP file type, returns a dictionary giving the
    extnames, the keywords and columns for that extension, and whether
    the entry is required (1) or recommended (0), and the specific
    values for the entry, if any.

    All logic is possible, as the requirement is given as a string
    that will be passed to eval() in a context where the object h will
    contain a class instance that contains the header and the
    functions

    h.Exists('KEY')
    h.hasVal('KEY','VAL')
    etc.  


    @return:

    """
    #
    # this function returns the  required and optional keywords and columns
    # as defined by OGIP 93-003 for a given extension
    #
    #
    # FOR CALDB File:
    # Define REQUIRED Keywords for CALDB file
    #
    reqkeys = {
        "TELESCOP":{"level":1,"req":"h.Exists('TELESCOP')"},
        "INSTRUME":{"level":1,"req":"h.Exists('INSTRUME')"},
        "DETNAM":  {"level":1,"req":"h.Exists('DETNAM')"},
        "FILTER":  {"level":1,"req":"h.Exists('FILTER')"},
        "CCLS0001":{"level":1,"req":"h.Exists('CCLS0001')"},
        "CDTP0001":{"level":1,"req":"h.Exists('CDTP0001')"},
        "CCNM0001":{"level":1,"req":"h.Exists('CCNM0001')"},
        "CBD*":    {"level":1,"req":"h.Exists('CBD*')"},  # BOUNDARY KEYWORD
        "CVSD0001":{"level":1,"req":"h.Exists('CVSD0001')"},
        "CVST0001":{"level":1,"req":"h.Exists('CVST0001')"},
        "CDES*" :  {"level":1,"req":"h.Exists('CDES*')"}, # can be given as single keyword or integer + fraction; either ok
        #
        #  Optional
        #
        "CTEL*":{"level":3,"req":"h.Exists('CTEL*')"},
        "CINS*":{"level":3,"req":"h.Exists('CINS*')"},
        "CDT*": {"level":3,"req":"h.Exists('CDT*')"},
        "CFI*": {"level":3,"req":"h.Exists('CFI*')"},
    }

    calfile = {'KEYWORDS':reqkeys,'COLUMNS':{}}

    extns={'REQUIRED':[],'OPTIONAL':[]}
    alt_extns={}


    ogip = {'EXTENSIONS':extns, 
            'ALT_EXTNS':alt_extns,
            'CALFILE': calfile,
            'REFERENCE':'OGIP/92-011',
            'REFTITLE':'Required and Recommended FITS keywords for Calibration Files',
            'REFURL':'http://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/docs/memos/cal_gen_92_011/cal_gen_92_011.html'} # for generic calibration file; EXTNAME not specified

    return ogip


