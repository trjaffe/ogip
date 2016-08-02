def ogip_general_checks(hdu):
    """
    Verifies that hdu conforms to the FITS standard and does some other general checks
    @param hdu:
    @return:
    """
    from astropy.time import Time
    timecards = ['DATE-OBS', 'DATE-END']
    for h in hdu:
        h.verify()
        for tc in timecards:
            try:
                Time(h.header[tc], format='fits')
            except ValueError:
                print "{0} = {1} is not a standard FITS time format".format(tc, hdu[1].header[tc])
            except KeyError:
                print "{0} not found in HEADER".format(tc)


