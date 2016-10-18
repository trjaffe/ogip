def ogip_dictionary_spectral():
    """

    For a given OGIP file type, returns a dictionary giving the
    extnames, the keywords and columns for that extension, and whether
    the entry is required (1) or recommended (0), and the specific
    values for the entry, if any.

    All logic is possible, as the requirement is given as a string that will be passed to eval() in a context where the object h will contain a class instance that contains the header and the functions 

    h.Exists('KEY')
    h.hasVal('KEY','VAL')
    etc.  

    """
    global status
    global REPORT

    """
    FOR SPECTRUM TABLE:
    """
    """
    Define REQUIRED Keywords for SPECTRUM TABLE
    """
    reqkeys = {
        'TELESCOPE':"h.Exists('TELESCOP')", 
        'INSTRUME':"h.Exists('INSTRUME')",
        'FILTER':"h.Exists('FILTER')",
        'EXPOSURE':"h.Exists('EXPOSURE')",
        'BACKFILE':"h.Exists('BACKFILE')",
        'CORRFILE':"h.Exists('CORRFILE')",
        'CORRSCAL':"h.Exists('CORRSCAL')",
        'RESPFILE':"h.Exists('RESPFILE')",
        'ANCRFILE':"h.Exists('ANCRFILE')",
        'HDUCLASS':"h.hasVal('HDUCLASS','OGIP')",  # OGIP is the allowed keyword value
        'HDUCLAS1':"h.hasVal('HDUCLAS1','SPECTRUM')",  # SPECTRUM is the allowed keyword value
        'HDUVERS':"h.hasVal('HDUVERS','1.2.1')",
        'POISSERR':"h.Exists('POISSERR') or h.hasCol('STAT_ERR')", 
        'CHANTYPE':"h.hasVal('CHANTYPE','PHA') or h.hasVal('CHANTYPE','PI')",
        'DETCHANS':"h.Exists('DETCHANS')"}

    """
    Define recommended Keywords
    """
    optkeys = {
        'XFLT*':"h.Exists('XFLT*')", # xspec filter descriptor
        'OBJECT':"h.Exists('OBJECT')",
        'RA-OBJ':"h.Exists('RA-OBJ')",
        'DEC-OBJ':"h.Exists('DEC-OBJ')",
        'DEC-OBJ':"h.Exists('DEC-OBJ')",
        'DATE-OBS':"h.Exists('DATE-OBS')",
        'DATE-END':"h.Exists('DATE-END')",
        'TIME-OBS':"h.Exists('TIME-OBS')", # time-obs can be included in date-obs
        'TIME-END':"h.Exists('TIME-END')", # time-end can be included in date-end
        'CREATOR':"h.Exists('CREATOR')",
        'HDUCLAS2':
        "   (h.hasVal('HDUCLAS2','TOTAL') and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
        "or (h.hasVal('HDUCLAS2','NET')   and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
        "or (h.hasVal('HDUCLAS2','BKG')   and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
        "or  h.hasVal('HDUCLAS2','DETECTOR')", 
        'HDUCLAS4':
        "(not h.hasCol('SPEC_NUM') and h.hasVal('HDUCLAS4','TYPE:I') ) "
        "or ( h.hasCol('SPEC_NUM') and h.hasVal('HDUCLAS4','TYPE:II') )",
#
#  TO BE FIXED: aren't in the document?
#
        'DETNAM':"h.Exists('DETNAM')", 
        'TLMIN*':"h.Exists('TLMIN*')", # required if channel numbering doesn't start at 1
        'TLMAX*':"h.Exists('TLMAX*')", # required if channel numbering doesn't start at 1
        'ONTIME':"h.Exists('ONTIME')",
        'TIMEZERO':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTART':"h.Exists('TSTART') or (h.Exists('TSTARTI') and h.Exists('TSTARTF'))",  # can be given as single keyword or integer + fraction; either ok
        'TSTOP':"h.Exists('TSTOP') or (h.Exists('TSTOPI') and h.Exists('TSTOPF'))",  # can be given as single keyword or integer + fraction; either ok
        'TIMESYS':"h.Exists('TIMESYS')",
        'TIMEUNIT':"h.Exists('TIMEUNIT')",
        'TIMEREF':"h.Exists('TIMEREF')",
        'SYS_ERR':"h.hasVal('SYS_ERR','0')",
        'QUALITY':"h.hasVal('QUALITY','0')",
        'GROUPING':"h.hasVal('GROUPING','0')",
        'CLOCKCOR':"h.Exists('CLOCKCOR')",
        'TIMVERSN':"h.Exists('TIMVERSN')",
        'AUTHOR':"h.Exists('AUTHOR')",
        'TASSIGN':"h.Exists('TASSIGN')",
        'TIERRELA':"h.Exists('TIERRELA')",
        'TIERABSO':"h.Exists('TIERABSO')",
        'ONTIME':"h.Exists('ONTIME')",
        'BACKAPP':"h.Exists('BACKAPP')",
        'VIGNAPP':"h.Exists('VIGNAPP')",
        'DEADAPP':"h.Exists('DEADAPP')",
        'EMIN*':"h.Exists('EMIN*')",
        'EMAX*':"h.Exists('EMAX*')",
        'BACKV*':"h.Exists('BACKV*')",
        'BACKE*':"h.Exists('BACKE*')",
        'DEADC*':"h.Exists('DEADC*')",
        'GEOAREA':"h.Exists('GEOAREA')",
        'VIGNET':"h.Exists('VIGNET')",
        'NPIXSOU':"h.Exists('NPIXSOU')",
        'NPIXBACK':"h.Exists('NPIXBACK')"
    }

    """
    Define Required Columns
    """
    reqcols = {
        'CHANNEL':"h.hasCol('CHANNEL')", # should be sequential
        'RATE|COUNTS':"h.hasCol('RATE') or h.hasCol('COUNTS')",  # means need either RATE or COUNTS column
        'STAT_ERR':"h.hasCol('STAT_ERR')", # optional if data given in counts per channel
        'SYS_ERR':"h.hasCol('SYS_ERR')", # can give SYS_ERR= 0 as keyword if no systematic error
        'QUALITY':"h.hasCol('QUALITY')", # can give QUALITY = 0 keyword if all data are good
        'GROUPING':"h.hasCol('GROUPING')", # can give GROUPING = 0 keyword if data are ungrouped
        'AREASCAL':"h.hasCol('AREASCAL')",    
        'BACKSCAL':"h.hasCol('BACKSCAL')", # often a measure of the area of the image from which data were extracted
        #
        # required for pha type 2 files, which we test for using SPEC_NUM column's existence
        #
        #'SPEC_NUM':"h.hasCol('SPEC_NUM')",
        'EXPOSURE':"not h.hasCol('SPEC_NUM') or h.hasCol('EXPOSURE')", # record of the exposure for each row in the type II file
        'BACKFILE':"not h.hasCol('SPEC_NUM') or h.hasCol('BACKFILE')", # background file for each row in the type II file
        'CORRFILE':"not h.hasCol('SPEC_NUM') or h.hasCol('CORRFILE')", # correction file for each row in the type II file
        'CORRSCAL':"not h.hasCol('SPEC_NUM') or h.hasCol('CORRSCAL')", # scaling for correction file for each row in the type II file
        'RESPFILE':"not h.hasCol('SPEC_NUM') or h.hasCol('RESPFILE')", # response file for each row in the type II file
        'ANCRFILE':"not h.hasCol('SPEC_NUM') or h.hasCol('ANCRFILE')" # ancillary file for each row in the type II file
    }

    """
    Define Optional Columns
    """
    optcols = {
        'DQF':"h.hasCol('DQF')", # combination of quality and grouping (not recommended)
        'ROWID':"h.hasCol('ROWID')" # optionally used for type II files
    }

    pha = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR GTI TABLE (OPTIONAL)
    """
    """
    Define Required Keywords FOR GTI TABLE
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')", 
        'INSTRUME':"h.Exists('INSTRUME')"
    }
    """
    Define optional Keywords
    """
    optkeys = {
        'DETNAM':"h.Exists('DETNAM')", 
        'FILTER':"h.Exists('FILTER')",
        'FILTER':"h.Exists('FILTER')",
        'RA*':"h.Exists('RA*')",
        'DEC*':"h.Exists('DEC*')",
        'TIMEZERO':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTART':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTOP':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and  h.Exists('TSTARTF') )",  # can be given as single keyword or integer + fraction; either ok
        'TIMESYS':"h.Exists('TIMESYS')",
        'TIMEUNIT':"h.Exists('TIMEUNIT')",
        'DATE-OBS':"h.Exists('DATE-OBS')",
        'DATE-END':"h.Exists('DATE-END')",
        'ONTIME':"h.Exists('ONTIME')",
        'HDUCLASS':"h.hasVal('HDUCLASS','OGIP')",
        'HDUCLAS1':"h.hasVal('HDUCLAS1','GTI')"
    }

    """
    Define Required Columns
    """
    reqcols = {
        'START':"h.hasCol('START')", 
        'STOP':"h.hasCol('STOP')"
    }
    """
    Define Optional Columns
    """
    optcols = {'TIMEDEL':"h.hasCol('TIMEDEL')"}

    gti={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}
    """
    FOR DETECTOR TABLE (optional)
    """
    """
    Define Required keywords
    """
    detector={'KEYWORDS':{'REQUIRED':{},'RECOMMENDED':{}}, 'COLUMNS':{'REQUIRED':[],'RECOMMENDED':[]} }
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
    history={'KEYWORDS':{'REQUIRED':{},'RECOMMENDED':{}}, 'COLUMNS':{'REQUIRED':[],'RECOMMENDED':[]} }
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
    #  Alternate extension names for those required.  Will generate an
    #  error but allow checking to continue.
    alt_extns={'SPECTRUM':['PHA','SPECTABLE']}

    #
    # create structure for pha file
    #
    ogip = {'EXTENSIONS':extns, 
            'ALT_EXTNS':alt_extns,
            'SPECTRUM':pha,
            'GTI':gti,
            'DETECTOR':detector, 
            'HISTORY':history,
            'REFERENCE':'OGIP/92-007',
            'REFURL':'https://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/summary/ogip_92_007_summary.html',
            'REFTITLE':'The OGIP Spectral File Format'}
    return ogip


