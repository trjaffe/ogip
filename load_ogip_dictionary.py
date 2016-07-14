def load_ogip_dictionary(type):
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

    Allowed OGIP types:
        type = TIMING, SPECTRAL, CALDB
    @param extname:
    @return:
    """

    import ogip

    global status
    global REPORT

    def spec():
        og = ogip.ogip_dictionary_spectral()
        return og
    def timing():
        og = ogip.ogip_dictionary_timing()
        return og
    def caldb():
        og = ogip.ogip_dictionary_caldb()
        return og
    def rmf():
        og = ogip.ogip_dictionary_rmf()
        return og
    def arf():
        og = ogip.ogip_dictionary_arf()
        return og

    defined_types={'SPECTRAL':spec, 'TIMING':timing,
                   'CALDB':caldb,'RMF':rmf, 'ARF':arf}
    key = type.strip().upper()
    try:
        # see https://bytebaker.com/2008/11/03/switch-case-statement-in-python/ for this way of
        # simulating a case/switch statement in python
        ogip=defined_types[key]()
    except KeyError:
        print "Dictionaries not defined for {0}; returning".format(key)
        ogip=0
    return ogip



if __name__ == "__main__":
    import ogip
    type='ARF'
    og=load_ogip_dictionary(type)
    print "For type = {1}, Found these EXTNAMES: {0}".format(og.keys(),type)
