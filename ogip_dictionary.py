from ogip_dictionary_timing import ogip_dictionary_timing
from ogip_dictionary_spectral import ogip_dictionary_spectral
from ogip_dictionary_caldb import ogip_dictionary_caldb
from ogip_dictionary_arf import ogip_dictionary_arf
from ogip_dictionary_rmf import ogip_dictionary_rmf
from ogip_dictionary_image import ogip_dictionary_image
import os
import json


def ogip_dictionary(type,meta_key=None):
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
        ogip=ogip_dictionary_timing()
    elif type.strip().upper() == 'SPECTRAL':
        ogip=ogip_dictionary_spectral()
    elif type.strip().upper() == 'CALDB':
        ogip=ogip_dictionary_caldb()
    elif type.strip().upper() == 'ARF':
        ogip=ogip_dictionary_arf()
    elif type.strip().upper() == 'RMF':
        ogip=ogip_dictionary_rmf()
    elif type.strip().upper() == 'IMAGE':
        ogip=ogip_dictionary_image()
    else:
        print "Currently defined for"
        print "Type = TIMING, SPECTRAL, CALDB, ARF, RMF, or IMAGE."
        ogip = 0

    #  Replace items in dictionary if found in the given meta data file.
    if meta_key is not None:
        metafile=os.path.join(os.path.dirname(__file__),("meta_%s.json"%meta_key))
        try:
            meta=json.load( open(metafile) )
        except:
            print("ERROR:  the meta data key %s does not correspond to a known meta-data JSON dictionary in %s." % (meta_key,os.path.dirname(__file__)) )
            raise

        #  The meta table is minimal, so things are only there if
        #  needed.  Check each of the keys that have either a single
        #  string value or an array value.  Then loop over keyword and
        #  column requirements for each extension defined.
        if "dicts" in meta and type in meta["dicts"]:
            for k in ('EXTENSIONS','ALT_EXTNS','REFERENCE','REFURL','REFTITLE'):
                if k in meta["dicts"]:  ogip[k]=meta["dicts"][k] 

            for extn in meta["dicts"][type]:
                if 'KEYWORDS' in meta["dicts"][type][extn]:  
                    for key,req in meta["dicts"][type][extn]['KEYWORDS'].iteritems():
                        ogip[extn]['KEYWORDS'][key]=req
                if 'COLUMNS' in meta["dicts"][type][extn]:  
                    for key,req in meta["dicts"][type][extn]['COLUMNS'].iteritems():
                        ogip[extn]['COLUMNS'][key]=req



    return ogip


