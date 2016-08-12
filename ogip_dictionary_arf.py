def ogip_dictionary_arf():
    """
    for a given OGIP ARF file,
    returns a dictionary giving the extnames, the keywords and columns for that extension, and whether the
    entry is required (1) or recommended (0), and the specific values for the entry, if any
    An asterisk (*) as the final character of a keyword indicates that the keyword root can have multiple values,
    for example: MJDREF (MJDREFI + MJDREFF), E_MIN1...E_MINn, etc
    Other Special Characters:
        a "+" is used if values are tied - if one appears the others need to appear ("MJDREFI + MJDREFF")
        a "|" separates names which can be used as alternates ("MJDREF | MJDREFI + MJDREFF")
        Square brackets "[ ]" mark required keyword values "HDUCLASS[OGIP]"

    @param extname:
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
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('FILTER')
    reqkeys.append('CHANTYPE[PHA|PI]')
    reqkeys.append('DETCHANS')
    reqkeys.append('HDUCLASS[OGIP]')
    reqkeys.append('HDUCLAS1[RESPONSE]')
    reqkeys.append('HDUCLAS2[SPECRESP]')
    reqkeys.append('HDUVERS[1.1.0]')
    reqkeys.append('TLMIN*')
    reqkeys.append('NUMGRP')
    reqkeys.append('NUMELT')
    reqkeys.append('CCLS0001[CPF]')
    reqkeys.append('CCNM0001[SPECRESP]')
    reqkeys.append('CDTP0001[DATA]')
    reqkeys.append('CVSD0001')
    reqkeys.append('CVST0001')
    reqkeys.append('CDES0001')

    """
    Define recommended Keywords
    """
    optkeys = ['PHAFILE']
    optkeys.append('LO_THRES') # minimum probability threshold in matrix (values < this are set to 0)
    optkeys.append('HDUCLAS3[REDIST|DETECTOR|FULL]') # required if channel numbering doesn't start at 1
    optkeys.append('RMFVERSN[1992A]')
    optkeys.append('HDUVERS1[1.1.0]')
    optkeys.append('HDUVERS2[1.2.0]')

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
    #
    # create structure for the ARF file
    #
    ogip = {'EXTENSIONS':extns,
            'SPECRESP':specresp,
            'REFERENCE':'OGIP/92-002',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html',
            'REFTITLE':'The Calibration Requirements for Spectral Analysis'}

    return ogip


