def ogip_dictionary_arf():
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
    """
    this function returns the  required and optional keywords and columns
    as defined by OGIP 92-002 and 92-002a
    """
    global status
    global REPORT

    """
    FOR the ARF file:
    """
    """
    Define REQUIRED Keywords for SPECRESP EXTENSION (note: EXTNAME is SPECRESP)
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')", 
        'INSTRUME':"h.Exists('INSTRUME')", 
        'FILTER':"h.Exists('FILTER')",
        'CHANTYPE':"h.hasVal('CHANTYPE','PHA') or h.hasVal('CHANTYPE','PI')",
        'DETCHANS':"h.Exists('DETCHANS')",
        'HDUCLASS':"h.hasVal('HDUCLASS','OGIP')",
        'HDUCLAS1':"h.hasVal('HDUCLAS1','RESPONSE')",
        'HDUCLAS2':"h.hasVal('HDUCLAS2','SPECRESP')",
        'HDUVERS':"h.hasVal('HDUVERS','1.1.0')",
        'TLMIN*':"h.Exists('TLMIN*')",
        'NUMGRP':"h.Exists('NUMGRP')",
        'NUMELT':"h.Exists('NUMELT')",
        'CCLS0001':"h.hasVal('CCLS0001','CPF')",
        'CCNM0001':"h.hasVal('CCNM0001','SPECRESP')",
        'CDTP0001':"h.hasVal('CDTP0001','DATA')",
        'CVSD0001':"h.Exists('CVSD0001')",
        'CVST0001':"h.Exists('CVST0001')",
        'CDES0001':"h.Exists('CDES0001')",
    }

    """
    Define recommended Keywords
    """
    optkeys = {
        'PHAFILE':"h.Exists('PHAFILE')",
        'LO_THRES':"h.Exists('LO_THRES')", # minimum probability threshold in matrix (values < this are set to 0)
        'HDUCLAS3':"h.hasVal('HDUCLAS3','REDIST') or h.hasVal('HDUCLAS3','DETECTOR') or h.hasVal('HDUCLAS3','FULL')", # required if channel numbering doesn't start at 1
        'RMFVERSN':"h.hasVal('RMFVERSN','1992A')",
        'HDUVERS1':"h.hasVal('HDUVERS1','1.1.0')",
        'HDUVERS2':"h.hasVal('HDUVERS2','1.2.0')",
    }

    """
    Define Required Columns
    """
    reqcols = ['ENERG_LO'] # lower energy bound of bin (keV)
    reqcols.append('ENERG_HI') # upper energy bound of bin (keV); generally ENERG_LO(J) = ENERG_HI(J-1)
    reqcols.append('SPECRESP') # the "effective area"


    """
    Define Optional Columns
    """
    optcols = [] # dispersion order for grating data

    specresp = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    extns={'REQUIRED':['SPECRESP'],'OPTIONAL':[]}
    #  Alternate extension names for those required.  Will generate an
    #  error but allow checking to continue.
    alt_extns={'SPECRESP':['ARF']}

    #
    # create structure for the ARF file
    #
    ogip = {'EXTENSIONS':extns,
            'ALT_EXTNS':alt_extns,
            'SPECRESP':specresp,
            'REFERENCE':'OGIP/92-002',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html',
            'REFTITLE':'The Calibration Requirements for Spectral Analysis'}

    return ogip


