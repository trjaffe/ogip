def ogip_dictionary_caldb():
    """
    for a given OGIP CALDB file,
    returns a dictionary giving the extnames, the keywords and columns for that extension, and whether the
    entry is required (1) or recommended (0), and the specific values for the entry, if any
    An asterisk (*) as the final character of a keyword indicates that the keyword root can have multiple values,
    for example: MJDREF (MJDREFI + MJDREFF), E_MIN1...E_MINn, etc
    Other Special Characters:
        a "+" is used if values are tied - if one appears the others need to appear ("MJDREFI + MJDREFF")
        a "|" separates names which can be used as alternates ("MJDREF | MJDREFI + MJDREFF")
        Square brackets "[ ]" mark required keyword values "HDUCLASS[OGIP]"

    Allowed OGIP types:
        type = TIMING
    @param extname:
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
    reqkeys = ['TELESCOP', 'INSTRUME', 'DETNAM', 'FILTER']
    reqkeys.append('CCLS0001')
    reqkeys.append('CDTP0001')
    reqkeys.append('CCNM0001')
    reqkeys.append('CBD*')  # BOUNDARY KEYWORDS
    reqkeys.append('CVSD0001')
    reqkeys.append('CVST0001')
    reqkeys.append('CDES*')  # can be given as single keyword or integer + fraction; either ok
    #
    # Define recommended Keywords
    #
    optkeys = ['CTEL*']
    optkeys.append('CINS*')
    optkeys.append('CDT*')
    optkeys.append('CFI*')
    calfile = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys},'COLUMNS':{'REQUIRED':[],'RECOMMENDED':[]}
    }

    extns={'REQUIRED':[],'OPTIONAL':[]}

    ogip = {'EXTENSIONS':extns, 
            'CALFILE': calfile,
            'REFERENCE':'OGIP/92-011',
            'REFTITLE':'Required and Recommended FITS keywords for Calibration Files',
            'REFURL':'http://heasarc.gsfc.nasa.gov/docs/heasarc/caldb/docs/memos/cal_gen_92_011/cal_gen_92_011.html#tab:keywordsum'} # for generic calibration file; EXTNAME not specified

    return ogip


