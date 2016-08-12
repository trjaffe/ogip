def ogip_dictionary_timing():
    """
    for a given OGIP file type (timing, etc),
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
    """
    this function returns the  required and optional keywords and columns
    as defined by OGIP 93-003 for a given extension
    """

    """
    FOR RATE TABLE:
    """
    """
    Define REQUIRED Keywords for RATE TABLE
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('DATE-OBS')
    reqkeys.append('DATE-END')
    reqkeys.append('ONTIME')
    reqkeys.append('TIMEZERO|TIMEZERI+TIMEZERF')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TSTART|TSTARTI+TSTARTF')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TSTOP|TSTOPI+TSTOPF')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TIMESYS')
    reqkeys.append('TIMEUNIT')
    reqkeys.append('TIMEREF')
    reqkeys.append('HDUCLASS[OGIP]')  # OGIP is the allowed keyword value
    reqkeys.append('HDUCLAS1[LIGHTCURVE]')  # LIGHTCURVE is the allowed keyword value
    """
    Define recommended Keywords
    """
    optkeys = ['DETNAM', 'FILTER']
    optkeys.append('RA*')
    optkeys.append('DEC*')
    optkeys.append('CLOCKCOR')
    optkeys.append('NUMBAND')
    optkeys.append('TIME-OBS')  # time-obs can be included in date-obs
    optkeys.append('TIME-END')  # time-end can be included in date-end
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
    reqcols = ['TIME']
    reqcols.append('RATE|COUNTS')  # means need either RATE or COUNTS column

    """
    Define Optional Columns
    """
    optcols = ['BACKV']
    optcols.append('BACKE')
    optcols.append('DEADC')

    rate = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR EVENTS TABLE:
    """
    """
    Define Required Keywords FOR EVENTS TABLE
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('DATE-OBS')
    reqkeys.append('DATE-END')
    reqkeys.append('ONTIME')
    reqkeys.append('TIMEZER*')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TSTART*')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TSTOP*')  # can be given as single keyword or integer + fraction; either ok
    reqkeys.append('TIMESYS')
    reqkeys.append('TIMEUNIT')
    reqkeys.append('HDUCLASS[OGIP]')
    reqkeys.append('HDUCLAS1[EVENTS]')

    """
    Define Optional Keywords
    """
    optkeys = ['DETNAM', 'FILTER']
    optkeys.append('FILTER')
    optkeys.append('RA*')
    optkeys.append('DEC*')
    optkeys.append('CLOCKCOR')
    optkeys.append('NUMBAND')
    optkeys.append('TIME-OBS')  # time-obs can be included in date-obs
    optkeys.append('TIME-END')  # time-end can be included in date-end
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
    """
    Define Required Columns
    """
    reqcols = ['TIME']
    """
    Define Optional Columns
    """
    optcols = ['X', 'Y', 'PHA', 'PI', 'DETX', 'DETY']

    events = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}
    """
    FOR GTI TABLE:
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
    FOR ENEBANDS TABLE:
    """
    """
    Define Required keywords
    """
    reqkeys = ['TELESCOP', 'INSTRUME']# no ENEBANDS-specific required keywords
    """
    Define Optional keywords
    """
    optkeys = ['DETNAM', 'FILTER']
    """
    Define Required Columns
    """
    reqcols = ['E_MIN', 'E_MAX']
    """
    Define Optional Columns
    """
    optcols = ['MINCHAN', 'MAXCHAN']

    eneband={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR TIMEREF TABLE:
    """
    """
    Define Required keywords
    """
    reqkeys = ['TELESCOP', 'INSTRUME']
    reqkeys.append('TSTART|TSTARTI+TSTARTF')
    reqkeys.append('TSTOP|TSTOPI+TSTARTF')
    reqkeys.append('TIMEZERO|TIMEZERI+TIMEZERF')
    reqkeys.append('TIMEUNIT')
    """
    Define Optional keywords
    """
    optkeys = ['DETNAM', 'FILTER']
    """
    Define Required Columns
    """
    reqcols = ['TIME']
    reqcols.append('REFEARTH|REFSUN|REFBSOLS|BARYTIME')
    """
    Define Optional Columns
    """
    optcols = []
    timeref={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    #  Define which extensions must be present, and which are optional
    extns={'REQUIRED':['RATE','EVENTS'],'OPTIONAL':['TIMEREF','ENEBAND','GTI']}

    ogip = {'EXTENSIONS':extns, 
            'RATE':rate, 
            'EVENTS':events, 
            'TIMEREF':timeref,
            'ENEBAND':eneband, 
            'GTI':gti,
            'REFERENCE':'OGIP/93-003',
            'REFTITLE':'The Proposed Timing FITS File Format for High Energy Astrophysics Data',
            'REFURL':'http://heasarc.gsfc.nasa.gov/FTP/caldb/docs/ogip/fits_formats/docs/rates/ogip_93_003/ogip_93_003.pdf'}

    return ogip


