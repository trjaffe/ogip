def ogip_dictionary_timing():
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

    """
    FOR RATE TABLE:
    """
    """
    Define REQUIRED Keywords for RATE TABLE
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')",
         'INSTRUME':"h.Exists('INSTRUME')",
        'DATE-OBS':"h.Exists('DATE-OBS')",
        'DATE-END':"h.Exists('DATE-END')",
        'ONTIME':"h.Exists('ONTIME')",
        'TIMEZERO':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTART':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTOP':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists('TSTOPF') )",  # can be given as single keyword or integer + fraction; either ok
        'TIMESYS':"h.Exists('TIMESYS')",
        'TIMEUNIT':"h.Exists('TIMEUNIT')",
        'TIMEREF':"h.Exists('TIMEREF')",
        'HDUCLASS':"h.hasVal('HDUCLASS','OGIP')",  # OGIP is the allowed keyword value
        'HDUCLAS1':"h.hasVal('HDUCLAS1','LIGHTCURVE')"  # LIGHTCURVE is the allowed keyword value
    }
    """
    Define recommended Keywords
    """
    optkeys = {
        'DETNAM':"h.Exists('DETNAM')",
        'FILTER':"h.Exists('FILTER')",
        'RA*':"h.Exists('RA*')",
        'DEC*':"h.Exists('DEC*')",
        'CLOCKCOR':"h.Exists('CLOCKCOR')",
        'NUMBAND':"h.Exists('NUMBAND')",
        'TIME-OBS':"h.Exists('TIME-OBS')",  # time-obs can be included in date-obs
        'TIME-END':"h.Exists('TIME-END')",  # time-end can be included in date-end
        'TIMVERSN':"h.Exists('TIMVERSN')",
        'OBJECT':"h.Exists('OBJECT')",
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
        'TIME':"h.hasCol('TIME')",
        'RATE|COUNTS':"h.hasCol('RATE') or h.hasCol('COUNTS')"
    }

    """
    Define Optional Columns
    """
    optcols = {
        'BACKV':"h.hasCol('BACKV')",
        'BACKE':"h.hasCol('BACKE')",
        'DEADC':"h.hasCol('DEADC')"
    }

    rate = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR EVENTS TABLE:
    """
    """
    Define Required Keywords FOR EVENTS TABLE
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')",
        'INSTRUME':"h.Exists('INSTRUME')",
        'DATE-OBS':"h.Exists('DATE-OBS')",
        'DATE-END':"h.Exists('DATE-END')",
        'ONTIME':"h.Exists('ONTIME')",
        'TIMEZER*':"h.Exists('TIMEZER*')",  # can be given as single keyword or integer + fraction; either ok
        'TSTART*':"h.Exists('TSTART*')",  # can be given as single keyword or integer + fraction; either ok
        'TSTOP*':"h.Exists('TSTOP*')",  # can be given as single keyword or integer + fraction; either ok
        'TIMESYS':"h.Exists('TIMESYS')",
        'TIMEUNIT':"h.Exists('TIMEUNIT')",
        'HDUCLASS':"h.hasVal('HDUCLASS','OGIP')",
        'HDUCLAS1':"h.hasVal('HDUCLAS1','EVENTS')"
    }

    """
    Define Optional Keywords
    """
    optkeys = {
        'DETNAM':"h.Exists('DETNAM')",
        'FILTER':"h.Exists('FILTER')",
        'RA*':"h.Exists('RA*')",
        'DEC*':"h.Exists('DEC*')",
        'CLOCKCOR':"h.Exists('CLOCKCOR')",
        'NUMBAND':"h.Exists('NUMBAND')",
        'TIME-OBS':"h.Exists('TIME-OBS')",  # time-obs can be included in date-obs
        'TIME-END':"h.Exists('TIME-END')",  # time-end can be included in date-end
        'TIMVERSN':"h.Exists('TIMVERSN')",
        'OBJECT':"h.Exists('OBJECT')",
        'AUTHOR':"h.Exists('AUTHOR')",
        'TASSIGN':"h.Exists('TASSIGN')",
        'TIERRELA':"h.Exists('TIERRELA')",
        'TIERABSO':"h.Exists('TIERABSO')",
        'ONTIME':"h.Exists('ONTIME')",
        'BACKAPP':"h.Exists('BACKAPP')",
        'VIGNAPP':"h.Exists('VIGNAPP')",
        'DEADAPP':"h.Exists('DEADAPP')"
    }
    """
    Define Required Columns
    """
    reqcols = {'TIME':"h.hasCol('TIME')"}
    """
    Define Optional Columns
    """
    optcols = {
        'X':"h.hasCol('X')", 
        'Y':"h.hasCol('Y')", 
        'PHA':"h.hasCol('PHA')", 
        'PI':"h.hasCol('PI')", 
        'DETX':"h.hasCol('DETX')", 
        'DETY':"h.hasCol('DETY')"
    }

    events = {'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}
    """
    FOR GTI TABLE:
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
        'RA*':"h.Exists('RA*')",
        'DEC*':"h.Exists('DEC*')",
        'TIMEZERO':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTART':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )",  # can be given as single keyword or integer + fraction; either ok
        'TSTOP':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists('TSTARTF') )",  # can be given as single keyword or integer + fraction; either ok
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
    FOR ENEBANDS TABLE:
    """
    """
    Define Required keywords
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')",
        'INSTRUME':"h.Exists('INSTRUME')" 
    }# no ENEBANDS-specific required keywords

    """
    Define Optional keywords
    """
    optkeys = {
        'DETNAM':"h.Exists('DETNAM')",
        'FILTER':"h.Exists('FILTER')"
    }
    """
    Define Required Columns
    """
    reqcols = {
        'E_MIN':"h.hasCol('E_MIN')", 
        'E_MAX':"h.hasCol('E_MAX')"
    }
    """
    Define Optional Columns
    """
    optcols = {
        'MINCHAN':"h.hasCol('MINCHAN')", 
        'MAXCHAN':"h.hasCol('MAXCHAN')"
    }

    eneband={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    """
    FOR TIMEREF TABLE:
    """
    """
    Define Required keywords
    """
    reqkeys = {
        'TELESCOP':"h.Exists('TELESCOP')",
        'INSTRUME':"h.Exists('INSTRUME')",
        'TSTART':"h.Exists('TSTART') or (h.Exists('TSTARTI') and h.Exists('TSTARTF') )",
        'TSTOP':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists(('TSTARTF') )",
        'TIMEZERO':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )",
        'TIMEUNIT':"h.Exists('TIMEUNIT')"
        }
    """
    Define Optional keywords
    """
    optkeys = {
        'DETNAM':"h.Exists('DETNAM')",
        'FILTER':"h.Exists('FILTER')"
    }
    """
    Define Required Columns
    """
    reqcols = {
        'TIME':"h.hasCol('TIME')",
        'REFEARTH|REFSUN|REFBSOLS|BARYTIME':"h.hasCol('REFEARTH') or h.hasCol('REFSUN') or h.hasCol('REFBSOLS') or h.hasCol('BARYTIME')", 
    }
    """
    Define Optional Columns
    """
    optcols = {}
    timeref={'KEYWORDS':{'REQUIRED':reqkeys,'RECOMMENDED':optkeys}, 'COLUMNS':{'REQUIRED':reqcols,'RECOMMENDED':optcols}}

    #  Define which extensions must be present, and which are optional
    extns={'REQUIRED':['RATE','EVENTS'],'OPTIONAL':['TIMEREF','ENEBAND','GTI']}
    #  Alternate extension names for those required.  Will generate an
    #  error but allow checking to continue.
    alt_extns={'RATE':['XTE_SA'],'EVENTS':['XTE_SE']}


    ogip = {'EXTENSIONS':extns, 
            'ALT_EXTNS':alt_extns,
            'RATE':rate, 
            'EVENTS':events, 
            'TIMEREF':timeref,
            'ENEBAND':eneband, 
            'GTI':gti,
            'REFERENCE':'OGIP/93-003',
            'REFTITLE':'The Proposed Timing FITS File Format for High Energy Astrophysics Data',
            'REFURL':'http://heasarc.gsfc.nasa.gov/FTP/caldb/docs/ogip/fits_formats/docs/rates/ogip_93_003/ogip_93_003.pdf'}

    return ogip


