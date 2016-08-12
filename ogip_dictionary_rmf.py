def ogip_dictionary_rmf():
    """
    for a given OGIP RMF file,
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
    FOR the RMF file:
    """
    """
    Define REQUIRED Keywords for RMF EXTENSION (note: EXTNAME can be either MATRIX or SPECRESP MATRIX)
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('FILTER')
    reqkeys.append('CHANTYPE[PHA|PI]')
    reqkeys.append('DETCHANS')
    reqkeys.append('HDUCLASS[OGIP]')
    reqkeys.append('HDUCLAS1[RESPONSE]')
    reqkeys.append('HDUCLAS2[RSP_MATRIX]')
    reqkeys.append('HDUVERS[1.3.0]')
    reqkeys.append('TLMIN*')
    reqkeys.append('NUMGRP')
    reqkeys.append('NUMELT')
    reqkeys.append('CCLS0001[CPF]')
    reqkeys.append('CCNM0001[MATRIX]')
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
    reqcols.append('N_GRP') # number of channel subsets for each row in the matrix
    reqcols.append('F_CHAN') # first channel number of  subset
    reqcols.append('N_CHAN') # number of channels in each subset
    reqcols.append('MATRIX')


    """
    Define Optional Columns
    """
    optcols = ['ORDER'] # dispersion order for grating data

    specresp = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR EBOUNDS TABLE
    """
    """
    Define Required Keywords FOR EBOUNDS TABLE
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('FILTER')
    reqkeys.append('CHANTYPE[PHA|PI]')
    reqkeys.append('DETCHANS')
    reqkeys.append('HDUCLASS[OGIP]')
    reqkeys.append('HDUCLAS1[RESPONSE]')
    reqkeys.append('HDUCLAS2[EBOUNDS]')
    reqkeys.append('HDUVERS[1.2.0]')
    reqkeys.append('CCLS0001[CPF]')
    reqkeys.append('CCNM0001[EBOUNDS]')
    reqkeys.append('CDTP0001[DATA]')
    reqkeys.append('CVSD0001')
    reqkeys.append('CVST0001')
    reqkeys.append('CDES0001')

    """
    Define optional Keywords
    """
    optkeys = ['PHAFILE']
    optkeys.append('RMFVERSN[1992A]')
    optkeys.append('HDUVERS1[1.1.0]')
    optkeys.append('HDUVERS2[1.2.0]')

    """
    Define Required Columns
    """
    reqcols = ['CHANNEL','E_MIN', 'E_MAX']
    """
    Define Optional Columns
    """
    optcols = []

    ebounds={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 
             'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    extns={'REQUIRED':['MATRIX'],'OPTIONAL':['EBOUNDS']}

    #
    # create structure for redistribution matrix file
    #
    ogip = {'EXTENSIONS':extns,
            'MATRIX':specresp,
            'EBOUNDS':ebounds,
            'REFERENCE':'OGIP/92-002, OGIP/92-002a',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html',
            'REFTITLE':'The Calibration Requirements for Spectral Analysis'}

    return ogip


