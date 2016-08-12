def ogip_dictionary_spectral():
    """
    for a given OGIP file type (PHA type I or type II),
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
    as defined by OGIP 92-007 for a given extension
    """
    global status
    global REPORT

    """
    FOR SPECTRUM TABLE:
    """
    """
    Define REQUIRED Keywords for SPECTRUM TABLE
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('FILTER')
    reqkeys.append('EXPOSURE')
    reqkeys.append('BACKFILE')
    reqkeys.append('CORRFILE')
    reqkeys.append('CORRSCAL')
    reqkeys.append('RESPFILE')
    reqkeys.append('ANCRFILE')
    reqkeys.append('HDUCLASS[OGIP]')  # OGIP is the allowed keyword value
    reqkeys.append('HDUCLAS1[SPECTRUM]')  # SPECTRUM is the allowed keyword value
    reqkeys.append('HDUVERS[1.2.1]')
    reqkeys.append('POISSERR')
    reqkeys.append('CHANTYPE[PHA|PI]')
    reqkeys.append('DETCHANS')

    """
    Define recommended Keywords
    """
    optkeys = ['DETNAM']
    optkeys.append('TLMIN*') # required if channel numbering doesn't start at 1
    optkeys.append('TLMAX*') # required if channel numbering doesn't start at 1
    optkeys.append('RA-OBJ')
    optkeys.append('DEC-OBJ')
    optkeys.append('XFLT*') # xspec filter descriptor
    optkeys.append('DATE-OBS')
    optkeys.append('DATE-END')
    optkeys.append('TIME-OBS') # time-obs can be included in date-obs
    optkeys.append('TIME-END') # time-end can be included in date-end
    optkeys.append('CREATOR')
    optkeys.append('HDUCLAS2[TOTAL|NET|BKG]')
    optkeys.append('HDUCLAS3[COUNT|RATE]')
    optkeys.append('ONTIME')
    optkeys.append('TIMEZERO|TIMEZERI+TIMEZERF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TSTART|TSTARTI+TSTARTF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TSTOP|TSTOPI+TSTOPF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TIMESYS')
    optkeys.append('TIMEUNIT')
    optkeys.append('TIMEREF')
    optkeys.append('SYS_ERR[0]')
    optkeys.append('QUALITY[0]')
    optkeys.append('GROUPING[0]')

    optkeys.append('CLOCKCOR')
    optkeys.append('TIMVERSN')
    optkeys.append('OBJECT')
    optkeys.append('AUTHOR')
    optkeys.append('TASSIGN')
    optkeys.append('TIERRELA')
    optkeys.append('TIERABSO')
    optkeys.append('ONTIME')
    optkeys.append('BACKAPP')
    optkeys.append('VIGNAPP')
    optkeys.append('DEADAPP')
    optkeys.append('EMIN*')
    optkeys.append('EMAX*')
    optkeys.append('BACKV*')
    optkeys.append('BACKE*')
    optkeys.append('DEADC*')
    optkeys.append('GEOAREA')
    optkeys.append('VIGNET')
    optkeys.append('NPIXSOU')
    optkeys.append('NPIXBACK')

    """
    Define Required Columns
    """
    reqcols = ['CHANNEL'] # should be sequential
    reqcols = ['SPEC_NUM'] # required for PHA type II files
    reqcols.append('RATE|COUNTS')  # means need either RATE or COUNTS column
    reqcols.append('STAT_ERR') # optional if data given in counts per channel
    reqcols.append('SYS_ERR') # can give SYS_ERR= 0 as keyword if no systematic error
    reqcols.append('QUALITY') # can give QUALITY = 0 keyword if all data are good
    reqcols.append('GROUPING') # can give GROUPING = 0 keyword if data are ungrouped
    reqcols.append('AREASCAL')
    reqcols.append('BACKSCAL') # often a measure of the area of the image from which data were extracted
    #
    # required for pha type 2 files
    #
    reqcols.append('EXPOSURE') # record of the exposure for each row in the type II file
    reqcols.append('BACKFILE') # background file for each row in the type II file
    reqcols.append('CORRFILE') # correction file for each row in the type II file
    reqcols.append('CORRSCAL') # scaling for correction file for each row in the type II file
    reqcols.append('RESPFILE') # response file for each row in the type II file
    reqcols.append('ANCRFILE') # ancillary file for each row in the type II file


    """
    Define Optional Columns
    """
    optcols = ['DQF'] # combination of quality and grouping (not recommended)
    optcols.append('ROWID') # optionally used for type II files


    pha = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR GTI TABLE (OPTIONAL)
    """
    """
    Define Required Keywords FOR GTI TABLE
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    """
    Define optional Keywords
    """
    optkeys = ['DETNAM', 'FILTER']
    optkeys.append('FILTER')
    optkeys.append('RA*')
    optkeys.append('DEC*')
    optkeys.append('TIMEZERO|TIMEZERI+TIMEZERF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TSTART|TSTARTI+TSTARTF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TSTOP|TSTOPI+TSTARTF')  # can be given as single keyword or integer + fraction; either ok
    optkeys.append('TIMESYS')
    optkeys.append('TIMEUNIT')
    optkeys = ['DATE-OBS']
    optkeys.append('DATE-END')
    optkeys.append('ONTIME')
    optkeys=['HDUCLASS[OGIP]']
    optkeys.append('HDUCLAS1[GTI]')

    """
    Define Required Columns
    """
    reqcols = ['START', 'STOP']
    """
    Define Optional Columns
    """
    optcols = ['TIMEDEL']

    gti={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}
    """
    FOR DETECTOR TABLE (optional)
    """
    """
    Define Required keywords
    """
    detector=dict()
    """
    Define Optional keywords
    """

    """
    Define Required Columns
    """

    """
    Define Optional Columns
    """

    """
    FOR HISTORY TABLE: (optional)
    """
    history=dict()
    """
    Define Required keywords
    """

    """
    Define Optional keywords
    """

    """
    Define Required Columns
    """

    """
    Define Optional Columns
    """
    extns={'REQUIRED':['SPECTRUM'], 'OPTIONAL':['HISTORY','DETECTOR','GTI']}
    #
    # create structure for pha file
    #
    ogip = {'EXTENSIONS':extns, 
            'SPECTRUM':pha,
            'GTI':gti,
            'DETECTOR':detector, 
            'HISTORY':history,
            'REFERENCE':'OGIP/92-007',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/summary/ogip_92_007_summary.html',
            'REFTITLE':'The OGIP Spectral File Format'}
    return ogip


