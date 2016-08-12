from ogip_dictionary_timing import ogip_dictionary_timing
from ogip_dictionary_spectral import ogip_dictionary_spectral
from ogip_dictionary_caldb import ogip_dictionary_caldb
from ogip_dictionary_arf import ogip_dictionary_arf
from ogip_dictionary_rmf import ogip_dictionary_rmf

def ogip_dictionary(type):
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
        type = TIMING, SPECTRAL, CALDB, ARF, RMF
    @param extname:
    @return:
    """
    """
    this function returns the  required and optional keywords and columns
    as defined by OGIP 93-003 (TIMING), 92-007 (SPECTRAL), 92-002 and 92-002a (ARF and RMF) for a given extension
    """

    if type.strip().upper() == 'TIMING':
        return ogip_dictionary_timing()
    elif type.strip().upper() == 'SPECTRAL':
        return ogip_dictionary_spectral()
    elif type.strip().upper() == 'CALDB':
        return ogip_dictionary_caldb()
    elif type.strip().upper() == 'ARF':
        return ogip_dictionary_arf()
    elif type.strip().upper() == 'RMF':
        return ogip_dictionary_rmf()
    else:
        print "Currently defined for"
        print "Type = TIMING, SPECTRAL, CALDB, ARF, or RMF."
        ogip = 0
    return ogip


