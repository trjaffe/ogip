def ogip_dictionary_spectral():
    """

    For a given OGIP file type, returns a dictionary giving the
    extnames, the keywords and columns for that extension, and whether
    the entry is required (level==3) or recommended (level!=3), and the specific
    values for the entry, if any.

    All logic is possible, as the requirement is given as a string
    that will be passed to eval() in a context where the object h will
    contain a class instance that contains the header and the
    functions

    h.Exists('KEY')
    h.hasVal('KEY','VAL')
    etc.

    """
    global status
    global REPORT

    """
    FOR SPECTRUM TABLE:

    Note that this attempts to handle both type I and type II cases,
    which means specifying requirements that involve both columns and
    keywords.  Here, we tag requirements as keywords that may include
    checking of a column, and likewise tag a column check that may
    need to check a keyword.  Any subsequent errors/warnings will have
    to be examined in detail.

    """
    """
    Define requirements for Keywords for SPECTRUM TABLE
    """
    reqkeys = {
        'TELESCOPE':{'level':1,'req':"h.Exists('TELESCOP')"},
        'INSTRUME': {'level':1,'req':"h.Exists('INSTRUME')"},
        'FILTER':   {'level':1,'req':"h.Exists('FILTER')"},
        # record of the exposure for each row in the type II file
        'EXPOSURE': {'level':1,'req':"h.Exists('EXPOSURE') or h.hasCol('EXPOSURE')"}, 
        # background file for each row in the type II file
        'BACKFILE': {'level':1,'req':"h.Exists('BACKFILE') or h.hasCol('BACKFILE')"},  
        # correction file for each row in the type II file
        'CORRFILE': {'level':1,'req':"h.Exists('CORRFILE') or h.hasCol('CORRFILE')"},  
        # scaling for correction file for each row in the type II file
        'CORRSCAL': {'level':1,'req':"h.Exists('CORRSCAL') or h.hasCol('CORRSCAL')"},  
        # response file for each row in the type II file
        'RESPFILE': {'level':1,'req':"h.Exists('RESPFILE') or h.hasCol('RESPFILE')"},  
        # ancillary file for each row in the type II file
        'ANCRFILE': {'level':1,'req':"h.Exists('ANCRFILE') or h.hasCol('ANCRFILE')"},  
        # OGIP is the allowed keyword value
        'HDUCLASS': {'level':1,'req':"h.hasVal('HDUCLASS','OGIP')"},   
        # SPECTRUM is the allowed keyword value
        'HDUCLAS1': {'level':1,'req':"h.hasVal('HDUCLAS1','SPECTRUM')"},   
        'HDUVERS':  {'level':1,'req':"h.Exists('HDUVERS')"}, 
        #  If there's a STAT_ERR column, POISSERR==F is only recommended.  Will be checked again below.  
        'POISSERR': {'level':1,'req':"( h.hasVal('POISSERR',True) and not h.hasCol('STAT_ERR') and h.hasCol('COUNTS') )"
                     " or ( h.hasCol('STAT_ERR') and not h.hasVal('POISSERR',True) )"}, 
        'CHANTYPE': {'level':1,'req':"h.hasVal('CHANTYPE','PHA',part=True) or h.hasVal('CHANTYPE','PI',part=True)"}, 
        'DETCHANS': {'level':1,'req':"h.Exists('DETCHANS')"}, 
        #
        #  Optional
        #
        # xspec filter descriptor
        'XFLT*':    {'level':2,'req':"h.Exists('XFLT*')"},  
        'OBJECT':   {'level':2,'req':"h.Exists('OBJECT')"}, 
        'RA-OBJ':   {'level':2,'req':"h.Exists('RA-OBJ')"}, 
        'DEC-OBJ':  {'level':2,'req':"h.Exists('DEC-OBJ')"}, 
        'DEC-OBJ':  {'level':2,'req':"h.Exists('DEC-OBJ')"}, 
        'DATE-OBS': {'level':2,'req':"h.Exists('DATE-OBS')"}, 
        'DATE-END': {'level':2,'req':"h.Exists('DATE-END')"}, 
        # time-obs can be included in date-obs
        'TIME-OBS': {'level':2,'req':"h.Exists('TIME-OBS')"},  
        # time-end can be included in date-end
        'TIME-END': {'level':2,'req':"h.Exists('TIME-END')"},  
        'CREATOR':  {'level':2,'req':"h.Exists('CREATOR')"}, 
        # warn if another version
        'HDUVERS':  {'level':2,'req':"h.hasVal('HDUVERS','1.2.1')"},  
        'HDUCLAS2': { 'level':2,'req':
        "   (h.hasVal('HDUCLAS2','TOTAL') and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
         "or (h.hasVal('HDUCLAS2','NET')   and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
        "or (h.hasVal('HDUCLAS2','BKG')   and (h.hasVal('HDUCLAS3','RATE') or h.hasVal('HDUCLAS3','COUNT')) ) "
        "or  h.hasVal('HDUCLAS2','DETECTOR')"},
        'HDUCLAS4': {'level':2,'req':
        "(not h.hasCol('SPEC_NUM') and h.hasVal('HDUCLAS4','TYPE:I') ) "
        "or ( h.hasCol('SPEC_NUM') and h.hasVal('HDUCLAS4','TYPE:II') )"},
        #  Above traps required case of POISSERR==T.  Here, warn if it
        #  should be F but is missing (but not if it should be T):
        'POISSERR2': {'level':2,'req':"(h.hasVal('POISSERR',False) and h.hasCol('STAT_ERR')) or not h.hasCol('STAT_ERR') "},  
        #
        #  TO BE FIXED: aren't in the document?
        #
        'DETNAM':  {'level':3,'req':"h.Exists('DETNAM')"},  
        # required if channel numbering doesn't start at 1
        'TLMIN*':  {'level':3,'req':"h.Exists('TLMIN*')"},  
        # required if channel numbering doesn't start at 1
        'TLMAX*':  {'level':3,'req':"h.Exists('TLMAX*')"},  
        'ONTIME':  {'level':3,'req':"h.Exists('ONTIME')"}, 
        # can be given as single keyword or integer + fraction; either ok
        'TIMEZERO':{'level':3,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},   
        'TSTART':  {'level':3,'req':"h.Exists('TSTART') or (h.Exists('TSTARTI') and h.Exists('TSTARTF'))"},   
        'TSTOP':   {'level':3,'req':"h.Exists('TSTOP') or (h.Exists('TSTOPI') and h.Exists('TSTOPF'))"},   
        'TIMESYS': {'level':3,'req':"h.Exists('TIMESYS')"}, 
        'TIMEUNIT':{'level':3,'req':"h.Exists('TIMEUNIT')"}, 
        'TIMEREF': {'level':3,'req':"h.Exists('TIMEREF')"}, 
        'CLOCKCOR':{'level':3,'req':"h.Exists('CLOCKCOR')"}, 
        'TIMVERSN':{'level':3,'req':"h.Exists('TIMVERSN')"}, 
        'AUTHOR':  {'level':3,'req':"h.Exists('AUTHOR')"}, 
        'TASSIGN': {'level':3,'req':"h.Exists('TASSIGN')"}, 
        'TIERRELA':{'level':3,'req':"h.Exists('TIERRELA')"}, 
        'TIERABSO':{'level':3,'req':"h.Exists('TIERABSO')"}, 
        'ONTIME':  {'level':3,'req':"h.Exists('ONTIME')"}, 
        'BACKAPP': {'level':3,'req':"h.Exists('BACKAPP')"}, 
        'VIGNAPP': {'level':3,'req':"h.Exists('VIGNAPP')"}, 
        'DEADAPP': {'level':3,'req':"h.Exists('DEADAPP')"}, 
        'EMIN*':   {'level':3,'req':"h.Exists('EMIN*')"}, 
        'EMAX*':   {'level':3,'req':"h.Exists('EMAX*')"}, 
        'BACKV*':  {'level':3,'req':"h.Exists('BACKV*')"}, 
        'BACKE*':  {'level':3,'req':"h.Exists('BACKE*')"}, 
        'DEADC*':  {'level':3,'req':"h.Exists('DEADC*')"}, 
        'GEOAREA': {'level':3,'req':"h.Exists('GEOAREA')"}, 
        'VIGNET':  {'level':3,'req':"h.Exists('VIGNET')"}, 
        'NPIXSOU': {'level':3,'req':"h.Exists('NPIXSOU')"}, 
        'NPIXBACK':{'level':3,'req':"h.Exists('NPIXBACK')"},     
    }

    """
    Define requirements for columns
    """
    reqcols = {
        # should be sequential
        'CHANNEL':    {'level':1,'req':"h.hasCol('CHANNEL')"},  
        # means need either RATE or COUNTS column
        'RATE|COUNTS':{'level':1,'req':"h.hasCol('RATE') or h.hasCol('COUNTS')"},   
        # optional if data given in counts per channel
        'STAT_ERR':   {'level':1,'req':" h.hasCol('STAT_ERR') or h.hasCol('COUNTS')"},  
        # can give SYS_ERR= 0 as keyword if no systematic error
        'SYS_ERR':    {'level':1,'req':"h.hasCol('SYS_ERR',part=True) or h.hasVal('SYS_ERR',0)"},  
        'SYS_ERR2':    {'level':2,'req':"h.hasCol('SYS_ERR') or h.hasVal('SYS_ERR',0)"},  
        # can give QUALITY = 0 keyword if all data are good
        'QUALITY':    {'level':1,'req':"h.hasCol('QUALITY') or h.hasCol('DQF') or h.hasVal('QUALITY',0)"},  
        # can give GROUPING = 0 keyword if data are ungrouped
        'GROUPING':   {'level':1,'req':"h.hasCol('GROUPING') or h.hasCol('DQF') or h.hasVal('GROUPING',0)"},  
        'AREASCAL':   {'level':1,'req':"h.hasCol('AREASCAL') or h.Exists('AREASCAL')"},     
        # often a measure of the area of the image from which data were extracted
        'BACKSCAL':   {'level':1,'req':"h.hasCol('BACKSCAL') or h.Exists('BACKSCAL')"},  
        #
        # Check for odd case of columns suited to type II spectra but
        # where there's no SPEC_NUM column, throw an error tagged
        # SPEC_NUM:  
        'SPEC_NUM':   {'level':1,'req':
        "(not h.hasCol('SPEC_NUM') and not ("
                       "   h.hasCol('EXPOSURE') or h.hasCol('BACKFILE') or h.hasCol('CORRFILE') "
                       "or h.hasCol('CORRSCAL') or h.hasCol('RESPFILE') or h.hasCol('ANCRFILE') "
                       ") )"
        "or h.hasCol('SPEC_NUM')"  }, 
        #
        #  Optional
        #
        # optionally used for type II files
        'ROWID':      {'level':2,'req':"not h.hasCol('SPEC_NUM') or h.hasCol('ROWID')"}, 
    }


    pha = {'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

    """
    FOR GTI TABLE (OPTIONAL)
    """
    """
    Define requirements for keywords FOR GTI TABLE
    """
    reqkeys = {
        'TELESCOP':{'level':1,'req':"h.Exists('TELESCOP')"},  
        'INSTRUME':{'level':1,'req':"h.Exists('INSTRUME')"},  
        'DETNAM':  {'level':2,'req':"h.Exists('DETNAM')"},  
        'FILTER':  {'level':2,'req':"h.Exists('FILTER')"}, 
        'FILTER':  {'level':2,'req':"h.Exists('FILTER')"}, 
        'RA*':     {'level':2,'req':"h.Exists('RA*')"}, 
        'DEC*':    {'level':2,'req':"h.Exists('DEC*')"}, 
        # can be given as single keyword or integer + fraction; either ok
        'TIMEZERO':{'level':2,'req':"h.Exists('TIMEZERO') or ( h.Exists('TIMEZERI') and h.Exists('TIMEZERF') )"},   
        # can be given as single keyword or integer + fraction; either ok
        'TSTART':  {'level':2,'req':"h.Exists('TSTART') or ( h.Exists('TSTARTI') and h.Exists('TSTARTF') )"},   
        # can be given as single keyword or integer + fraction; either ok
        'TSTOP':   {'level':2,'req':"h.Exists('TSTOP') or ( h.Exists('TSTOPI') and  h.Exists('TSTARTF') )"},   
        'TIMESYS': {'level':2,'req':"h.Exists('TIMESYS')"}, 
        'TIMEUNIT':{'level':2,'req':"h.Exists('TIMEUNIT')"}, 
        'DATE-OBS':{'level':2,'req':"h.Exists('DATE-OBS')"}, 
        'DATE-END':{'level':2,'req':"h.Exists('DATE-END')"}, 
        'ONTIME':  {'level':2,'req':"h.Exists('ONTIME')"}, 
        'HDUCLASS':{'level':2,'req':"h.hasVal('HDUCLASS','OGIP')"}, 
        'HDUCLAS1':{'level':2,'req':"h.hasVal('HDUCLAS1','GTI')"},     
    }

    """
    Define Required Columns
    """
    reqcols = {
        'START':  {'level':1,'req':"h.hasCol('START')"},  
        'STOP':   {'level':1,'req':"h.hasCol('STOP')"},     
        'TIMEDEL':{'level':2,'req':"h.hasCol('TIMEDEL')"},     
    }

    gti={'KEYWORDS':reqkeys,'COLUMNS':reqcols}
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
    history={'KEYWORDS':{},'COLUMNS':{} }
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


