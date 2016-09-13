def ogip_dictionary_caldb():
    """

    For a given OGIP file type, returns a dictionary giving the
    extnames, the keywords and columns for that extension, and whether
    the entry is required (1) or recommended (0), and the specific
    values for the entry, if any.

    All logic is possible, as the requirement is given as a string that will be passed to eval() in a context where the object h will contain a class instance that contains the header and the functions 

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
        'TELESCOP':"h.Exists('TELESCOP')",
        'INSTRUME':"h.Exists('INSTRUME')",
        'DETNAM':"h.Exists('DETNAM')",
        'FILTER':"h.Exists('FILTER')",
        'CCLS0001':"h.Exists('CCLS0001')",
        'CDTP0001':"h.Exists('CDTP0001')",
        'CCNM0001':"h.Exists('CCNM0001')",
        'CBD*':"h.Exists('CBD*')",  # BOUNDARY KEYWORD
        'CVSD0001':"h.Exists('CVSD0001')",
        'CVST0001':"h.Exists('CVST0001')",
        'CDES*' :"h.Exists('CDES*')" # can be given as single keyword or integer + fraction; either ok
    }

    #
    # Define recommended Keywords
    #
    optkeys = {
        'CTEL*':"h.Exists('CTEL*')",
        'CINS*':"h.Exists('CINS*')",
        'CDT*':"h.Exists('CDT*')",
        'CFI*':"h.Exists('CFI*')",
    }

    calfile = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys},'COLUMNS':{'REQUIRED':[],'RECOMMENDED':[]}
    }

    extns={'REQUIRED':[],'OPTIONAL':[]}
    alt_extns={}


    ogip = {'EXTENSIONS':extns, 
            'ALT_EXTNS':alt_extns,
            'CALFILE': calfile,
            'REFERENCE':'OGIP/92-011',
            'REFTITLE':'Required and Recommended FITS keywords for Calibration Files',
            'REFURL':'http://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/docs/memos/cal_gen_92_011/cal_gen_92_011.html'} # for generic calibration file; EXTNAME not specified

    return ogip


