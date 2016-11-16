def ogip_dictionary_rmf():
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
    """
    this function returns the  required and optional keywords and columns
    as defined by OGIP 92-002 and 92-002a
    """
    global status
    global REPORT

    """
    FOR the RMF file:
    """
    """
    Define requirements for keywords for RMF extension (note: EXTNAME can be either MATRIX or SPECRESP MATRIX)
    """
    reqkeys = {
        "TELESCOP":{"level":1,"req":"h.Exists('TELESCOP')"},
        "INSTRUME":{"level":1,"req":"h.Exists('INSTRUME')"},
        "CHANTYPE":{"level":1,"req":"h.hasVal('CHANTYPE','PHA') or h.hasVal('CHANTYPE','PI')"},
        "DETCHANS":{"level":1,"req":"h.Exists('DETCHANS')"},
        "HDUCLASS":{"level":1,"req":"h.hasVal('HDUCLASS','OGIP')"},
        "HDUCLAS1":{"level":1,"req":"h.hasVal('HDUCLAS1','RESPONSE')"},
        "HDUCLAS2":{"level":1,"req":"h.hasVal('HDUCLAS2','RSP_MATRIX')"},
        "HDUVERS": {"level":1,"req":"h.Exists('HDUVERS')"},
        "TLMIN*":  {"level":1,"req":"h.Exists('TLMIN*')"},
        "NUMGRP":  {"level":1,"req":"h.Exists('NUMGRP')"},
        "NUMELT":  {"level":1,"req":"h.Exists('NUMELT')"},
        "CCLS0001":{"level":1,"req":"h.hasVal('CCLS0001','CPF')"},
        "CCNM0001":{"level":1,"req":"h.hasVal('CCNM0001','MATRIX')"},
        "CDTP0001":{"level":1,"req":"h.hasVal('CDTP0001','DATA')"},
        "CVSD0001":{"level":1,"req":"h.Exists('CVSD0001')"},
        "CVST0001":{"level":1,"req":"h.Exists('CVST0001')"},
        "CDES0001":{"level":1,"req":"h.Exists('CDES0001')"},
        #
        #  Optional
        #
        "FILTER":  {"level":3,"req":"h.Exists('FILTER')"},
        "PHAFILE": {"level":3,"req":"h.Exists('PHAFILE')"},
        # minimum probability threshold in matrix (values < this are set to 0)
        "LO_THRES":{"level":3,"req":"h.Exists('LO_THRES')"}, 
        # required if channel numbering doesn"t start at 
        "HDUCLAS3":{"level":3,"req":"h.hasVal('HDUCLAS3','REDIST') or h.hasVal('HDUCLAS3','DETECTOR') or h.hasVal('HDUCLAS3','FULL')"}, 
        "RMFVERSN":{"level":3,"req":"h.hasVal('RMFVERSN','1992A')"},
        "HDUVERS": {"level":3,"req":"h.hasVal('HDUVERS','1.3.0')"},
        "HDUVERS1":{"level":3,"req":"h.hasVal('HDUVERS1','1.1.0')"},
        "HDUVERS2":{"level":3,"req":"h.hasVal('HDUVERS2','1.2.0')"}
    }

    """
    Define requirements for columns
    """
    reqcols = {
        # lower energy bound of bin (keV)
        "ENERG_LO":{"level":1,"req":"h.hasCol('ENERG_LO')"},
        # upper energy bound of bin (keV); generally ENERG_LO(J) = ENERG_HI(J-1)
        "ENERG_HI":{"level":1,"req":"h.hasCol('ENERG_HI')"}, 
        # number of channel subsets for each row in the matrix
        "N_GRP":   {"level":1,"req":"h.hasCol('N_GRP')"},
        # first channel number of  subset
        "F_CHAN":  {"level":1,"req":"h.hasCol('F_CHAN')"}, 
        # number of channels in each subset
        "N_CHAN":  {"level":1,"req":"h.hasCol('N_CHAN')"}, 
        "MATRIX":  {"level":1,"req":"h.hasCol('MATRIX')"},
        #
        #  Optional
        #
        # dispersion order for grating data
        "ORDER":   {"level":3,"req":"h.hasCol('ORDER')"}
    }
    
    specresp = {'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

    """
    FOR EBOUNDS TABLE
    """
    """
    Define requirements for keywords for EBOUNDS table
    """
    reqkeys = {
        "TELESCOP":{"level":1,"req":"h.Exists('TELESCOP')"},
        "INSTRUME":{"level":1,"req":"h.Exists('INSTRUME')"},
        "CHANTYPE":{"level":1,"req":"h.hasVal('CHANTYPE','PHA') or h.hasVal('CHANTYPE','PI')"},
        "DETCHANS":{"level":1,"req":"h.Exists('DETCHANS')"},
        "HDUCLASS":{"level":1,"req":"h.hasVal('HDUCLASS','OGIP')"},
        "HDUCLAS1":{"level":1,"req":"h.hasVal('HDUCLAS1','RESPONSE')"},
        "HDUCLAS2":{"level":1,"req":"h.hasVal('HDUCLAS2','EBOUNDS')"},
        "HDUVERS": {"level":1,"req":"h.Exists('HDUVERS')"},
        "CCLS0001":{"level":1,"req":"h.hasVal('CCLS0001','CPF')"},
        "CCNM0001":{"level":1,"req":"h.hasVal('CCNM0001','EBOUNDS')"},
        "CDTP0001":{"level":1,"req":"h.hasVal('CDTP0001','DATA')"},
        "CVSD0001":{"level":1,"req":"h.Exists('CVSD0001')"},
        "CVST0001":{"level":1,"req":"h.Exists('CVST0001')"},
        "CDES0001":{"level":1,"req":"h.Exists('CDES0001')"},
        #
        #  Optional
        #
        "FILTER":  {"level":3,"req":"h.Exists('FILTER')"},
        "PHAFILE": {"level":3,"req":"h.Exists('PHAFILE')"},
        "RMFVERSN":{"level":3,"req":"h.hasVal('RMFVERSN','1992A')"},
        "HDUVERS": {"level":3,"req":"h.hasVal('HDUVERS','1.2.0]')"},
        "HDUVERS1":{"level":3,"req":"h.hasVal('HDUVERS1','1.1.0]')"},
        "HDUVERS2":{"level":3,"req":"h.hasVal('HDUVERS2','1.2.0]')"}
    }

    """
    Define requirements for columns
    """
    reqcols = {
        "CHANNEL":{"level":1,"req":"h.hasCol('CHANNEL')"},
        "E_MIN":{"level":1,"req":"h.hasCol('E_MIN')"}, 
        "E_MAX":{"level":1,"req":"h.hasCol('E_MAX')"}
    }
 
    ebounds={'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

    extns={'REQUIRED':['MATRIX'],'OPTIONAL':['EBOUNDS']}
    #  Alternate extension names for those required.  Will generate an
    #  error but allow checking to continue.
    alt_extns={'MATRIX':[]}

    #
    # create structure for redistribution matrix file
    #
    ogip = {'EXTENSIONS':extns,
            'ALT_EXTNS':alt_extns,
            'MATRIX':specresp,
            'EBOUNDS':ebounds,
            'REFERENCE':'OGIP/92-002, OGIP/92-002a',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html',
            'REFTITLE':'The Calibration Requirements for Spectral Analysis'}

    return ogip


