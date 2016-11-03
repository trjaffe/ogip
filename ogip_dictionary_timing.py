def ogip_dictionary_timing():
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

    """

    """
    FOR RATE TABLE:
    """
    """
    Define requirements for  Keywords for RATE table
    """
    reqkeys = {
        'TELESCOP':{"level":1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,'req':"h.Exists('INSTRUME')"},
        'DATE-OBS':{"level":1,'req':"h.Exists('DATE-OBS')"},
        'DATE-END':{"level":1,'req':"h.Exists('DATE-END')"},
        # can be given as single keyword or integer + fraction; either ok
        'TIMEZERO':{"level":1,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTART':  {"level":1,'req':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTOP':   {"level":1,'req':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists('TSTOPF') )"},  
        'TIMESYS': {"level":1,'req':"h.Exists('TIMESYS')"},
        'TIMEUNIT':{"level":1,'req':"h.Exists('TIMEUNIT')"},
        'TIMEREF': {"level":1,'req':"h.Exists('TIMEREF')"},
        # OGIP is the allowed keyword value
        'HDUCLASS':{"level":1,'req':"h.hasVal('HDUCLASS','OGIP')"},  
        # LIGHTCURVE is the allowed keyword value
        'HDUCLAS1':{"level":1,'req':"h.hasVal('HDUCLAS1','LIGHTCURVE')"},
        #
        #  Optional
        #
        'DETNAM':   {"level":2,'req':"h.Exists('DETNAM')"},
        'FILTER':   {"level":2,'req':"h.Exists('FILTER')"},
        'RA*':      {"level":2,'req':"h.Exists('RA*')"},
        'DEC*':     {"level":2,'req':"h.Exists('DEC*')"},
        'CLOCKCOR': {"level":2,'req':"h.Exists('CLOCKCOR')"},
        'NUMBAND':  {"level":2,'req':"h.Exists('NUMBAND')"},
        # time-obs can be included in date-obs
        'TIME-OBS': {"level":2,'req':"h.Exists('TIME-OBS')"},  
        # time-end can be included in date-end
        'TIME-END': {"level":2,'req':"h.Exists('TIME-END')"},  
        'TIMVERSN': {"level":2,'req':"h.Exists('TIMVERSN')"},
        'OBJECT':   {"level":2,'req':"h.Exists('OBJECT')"},
        'AUTHOR':   {"level":2,'req':"h.Exists('AUTHOR')"},
        'TASSIGN':  {"level":2,'req':"h.Exists('TASSIGN')"},
        'TIERRELA': {"level":2,'req':"h.Exists('TIERRELA')"},
        'TIERABSO': {"level":2,'req':"h.Exists('TIERABSO')"},
        'ONTIME':   {"level":2,'req':"h.Exists('ONTIME')"},
        'BACKAPP':  {"level":2,'req':"h.Exists('BACKAPP')"},
        'VIGNAPP':  {"level":2,'req':"h.Exists('VIGNAPP')"},
        'DEADAPP':  {"level":2,'req':"h.Exists('DEADAPP')"},
        'EMIN*':    {"level":2,'req':"h.Exists('EMIN*')"},
        'EMAX*':    {"level":2,'req':"h.Exists('EMAX*')"},
        'BACKV*':   {"level":2,'req':"h.Exists('BACKV*')"},
        'BACKE*':   {"level":2,'req':"h.Exists('BACKE*')"},
        'DEADC*':   {"level":2,'req':"h.Exists('DEADC*')"},
        'GEOAREA':  {"level":2,'req':"h.Exists('GEOAREA')"},
        'VIGNET':   {"level":2,'req':"h.Exists('VIGNET')"},
        'NPIXSOU':  {"level":2,'req':"h.Exists('NPIXSOU')"},
        'NPIXBACK': {"level":2,'req':"h.Exists('NPIXBACK')"}
    }

    """
    Define requirements for columns
    """
    reqcols = {
        'TIME':       {"level":1,'req':"h.hasCol('TIME')"},
        'RATE|COUNTS':{"level":1,'req':"h.hasCol('RATE') or h.hasCol('COUNTS')"},
        'BACKV':      {"level":2,'req':"h.hasCol('BACKV')"},
        'BACKE':      {"level":2,'req':"h.hasCol('BACKE')"},
        'DEADC':      {"level":2,'req':"h.hasCol('DEADC')"}
    }

    rate = {'KEYWORDS':reqkeys, 'COLUMNS':reqcols}






    """
    FOR EVENTS TABLE:
    """
    """
    Define requirements for keywords for EVENTS table
    """
    reqkeys = {
        'TELESCOP':{"level":1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,'req':"h.Exists('INSTRUME')"},
        'DATE-OBS':{"level":1,'req':"h.Exists('DATE-OBS')"},
        'DATE-END':{"level":1,'req':"h.Exists('DATE-END')"},
        # can be given as single keyword or integer + fraction; either ok
        'TIMEZERO':{"level":1,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTART':  {"level":1,'req':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTOP':   {"level":1,'req':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists('TSTOPF') )"},  
        'TIMESYS': {"level":1,'req':"h.Exists('TIMESYS')"},
        'TIMEUNIT':{"level":1,'req':"h.Exists('TIMEUNIT')"},
        'HDUCLASS':{"level":1,'req':"h.hasVal('HDUCLASS','OGIP')"},
        'HDUCLAS1':{"level":1,'req':"h.hasVal('HDUCLAS1','EVENTS')"},
        #
        #  Optional
        #
        'ONTIME':  {"level":2,'req':"h.Exists('ONTIME')"},
        'DETNAM':  {"level":2,'req':"h.Exists('DETNAM')"},
        'FILTER':  {"level":2,'req':"h.Exists('FILTER')"},
        'RA*':     {"level":2,'req':"h.Exists('RA*')"},
        'DEC*':    {"level":2,'req':"h.Exists('DEC*')"},
        'CLOCKCOR':{"level":2,'req':"h.Exists('CLOCKCOR')"},
        'NUMBAND': {"level":2,'req':"h.Exists('NUMBAND')"},
        # time-obs can be included in date-obs
        'TIME-OBS':{"level":2,'req':"h.Exists('TIME-OBS')"},  
        # time-end can be included in date-end
        'TIME-END':{"level":2,'req':"h.Exists('TIME-END')"},  
        'TIMVERSN':{"level":2,'req':"h.Exists('TIMVERSN')"},
        'OBJECT':  {"level":2,'req':"h.Exists('OBJECT')"},
        'AUTHOR':  {"level":2,'req':"h.Exists('AUTHOR')"},
        'TASSIGN': {"level":2,'req':"h.Exists('TASSIGN')"},
        'TIERRELA':{"level":2,'req':"h.Exists('TIERRELA')"},
        'TIERABSO':{"level":2,'req':"h.Exists('TIERABSO')"},
        'BACKAPP': {"level":2,'req':"h.Exists('BACKAPP')"},
        'VIGNAPP': {"level":2,'req':"h.Exists('VIGNAPP')"},
        'DEADAPP': {"level":2,'req':"h.Exists('DEADAPP')"}
    }
    """
    Define requirements for  columns
    """
    reqcols = {
        'TIME':{"level":1,'req':"h.hasCol('TIME')"},
        #
        #   Optional
        #
        'X':   {"level":2,'req':"h.hasCol('X')"}, 
        'Y':   {"level":2,'req':"h.hasCol('Y')"}, 
        'PHA': {"level":2,'req':"h.hasCol('PHA')"}, 
        'PI':  {"level":2,'req':"h.hasCol('PI')"}, 
        'DETX':{"level":2,'req':"h.hasCol('DETX')"}, 
        'DETY':{"level":2,'req':"h.hasCol('DETY')"}
     }

    events = {'KEYWORDS':reqkeys, 'COLUMNS':reqcols}





    """
    FOR GTI TABLE:
    """
    """
    Define requirements for  keywords for GTI table
    """
    reqkeys = {
        'TELESCOP':{"level":1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,'req':"h.Exists('INSTRUME')"},
        #
        #  Optional
        #
        'DETNAM':  {"level":2,'req':"h.Exists('DETNAM')"},
        'FILTER':  {"level":2,'req':"h.Exists('FILTER')"},
        'RA*':     {"level":2,'req':"h.Exists('RA*')"},
        'DEC*':    {"level":2,'req':"h.Exists('DEC*')"},
        # can be given as single keyword or integer + fraction; either ok
        'TIMEZERO':{"level":2,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTART':  {"level":2,'req':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )"},  
        # can be given as single keyword or integer + fraction; either ok
        'TSTOP':   {"level":2,'req':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists('TSTARTF') )"},  
        'TIMESYS': {"level":2,'req':"h.Exists('TIMESYS')"},
        'TIMEUNIT':{"level":2,'req':"h.Exists('TIMEUNIT')"},
        'DATE-OBS':{"level":2,'req':"h.Exists('DATE-OBS')"},
        'DATE-END':{"level":2,'req':"h.Exists('DATE-END')"},
        'ONTIME':  {"level":2,'req':"h.Exists('ONTIME')"},
        'HDUCLASS':{"level":2,'req':"h.hasVal('HDUCLASS','OGIP')"},
        'HDUCLAS1':{"level":2,'req':"h.hasVal('HDUCLAS1','GTI')"}
    }

    """
    Define requirements for  columns
    """
    reqcols = {
        'START':{"level":1,'req':"h.hasCol('START')"}, 
        'STOP': {"level":1,'req':"h.hasCol('STOP')"},
        # 
        #  Optional
        # 
        'TIMEDEL':{"level":2,'req':"h.hasCol('TIMEDEL')"}
    }

    gti={'KEYWORDS':reqkeys, 'COLUMNS':reqcols}




    """
    FOR ENEBANDS TABLE:
    """
    """
    Define requirements for keywords
    """
    reqkeys = {
        'TELESCOP':{"level":1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,'req':"h.Exists('INSTRUME')"}, 
        #
        #  Optional
        #
        'DETNAM':{"level":2,'req':"h.Exists('DETNAM')"},
        'FILTER':{"level":2,'req':"h.Exists('FILTER')"}
    }
    """
    Define requirements for columns
    """
    reqcols = {
        'E_MIN':{"level":1,'req':"h.hasCol('E_MIN')"}, 
        'E_MAX':{"level":1,'req':"h.hasCol('E_MAX')"},
        #
        #  Optional
        #
        'MINCHAN':{"level":2,'req':"h.hasCol('MINCHAN')"}, 
        'MAXCHAN':{"level":2,'req':"h.hasCol('MAXCHAN')"}
    }

    eneband={'KEYWORDS':reqkeys, 'COLUMNS':reqcols}






    """
    FOR TIMEREF TABLE:
    """
    """
    Define requirements for keywords
    """
    reqkeys = {
        'TELESCOP':{"level":1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,'req':"h.Exists('INSTRUME')"},
        'TSTART':  {"level":1,'req':"h.Exists('TSTART') or (h.Exists('TSTARTI') and h.Exists('TSTARTF') )"},
        'TSTOP':   {"level":1,'req':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and h.Exists(('TSTARTF') )"},
        'TIMEZERO':{"level":1,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},
        'TIMEUNIT':{"level":1,'req':"h.Exists('TIMEUNIT')"},
        #
        #  Optional
        # 
        'DETNAM':{"level":2,'req':"h.Exists('DETNAM')"},
        'FILTER':{"level":2,'req':"h.Exists('FILTER')"}
    }
    """
    Define requirements for columns
    """
    reqcols = {
        'TIME':{"level":1,'req':"h.hasCol('TIME')"},
        'REFEARTH|REFSUN|REFBSOLS|BARYTIME':{"level":1,'req':"h.hasCol('REFEARTH') or h.hasCol('REFSUN') or h.hasCol('REFBSOLS') or h.hasCol('BARYTIME')"}, 
    }
    timeref={'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

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


