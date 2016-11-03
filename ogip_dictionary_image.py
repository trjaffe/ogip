def ogip_dictionary_image():
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
    as defined by OGIP.  Reference file TBD.
    """
    global status
    global REPORT

    """
    FOR the IMAGE file:
    """
    """
    Define requirements for keywords for PRIMARY or IMAGE extension 
    """
    reqkeys = {
        'TELESCOP':{"level":1,"req":"h.Exists('TELESCOP')"},
        'INSTRUME':{"level":1,"req":"h.Exists('INSTRUME')"},
        'FILTER':  {"level":1,"req":"h.Exists('FILTER')"},
        'HDUCLASS':{"level":1,"req":"h.hasVal('HDUCLASS','OGIP')"},
 
    }

    """
    Define requirements for columns
    """
    reqcols = {
    }
    
    image = {'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

    """
    For GTI extension
    """
    """
    Define requirements for keywords for EBOUNDS table
    """
    reqkeys = {
    }

    """
    Define requirements for columns
    """
    reqcols = {
    }
 
    gti={'KEYWORDS':reqkeys, 'COLUMNS':reqcols}

    extns={'REQUIRED':[''],'OPTIONAL':['GTI']}
    #  Alternate extension names for those required.  Will generate an
    #  error but allow checking to continue.
    alt_extns={}

    #
    # create structure for redistribution matrix file
    #
    ogip = {'EXTENSIONS':extns,
            'ALT_EXTNS':alt_extns,
            'IMAGE':image,
            'GTI':gti,
            'REFERENCE':'',
            'REFURL':'',
            'REFTITLE':''}

    return ogip


