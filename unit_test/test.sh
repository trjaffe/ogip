#!/bin/bash
echo "##################################################################"
echo "#" 
echo "#  This is the unit test for the OGIP ogip_check utility.  It runs"
echo "#  through a set of test files, runs the checks with outputs"
echo "#  redirected into logs in the 'out' directory.  It compares these"
echo "#  logs to the reference set in 'ref' and flags any differences.  "
echo "#"
echo "##################################################################"
echo ""

#  So it can be interrupted with ^c
trap '{ echo "ogip_check interrupted;  exiting."; exit; }' INT


if [[ -e out ]]; then
    rm -r out
fi
mkdir out

let errors=0

echo "##################################################################"
echo "# Basic tests, i.e., run each file type with no arguments:"
for file in $( ls inputs/* );
do
    echo ""
    file=`echo ${file} | awk -F/ '{print $2}'`
    echo "Checking file ${file}"
    ../ogip_check inputs/${file} &> out/${file}.ogip_check.log
    retval=$?
    echo "Return status was $retval"
    if [[ "$retval" != "0" ]];  then
       echo "ERROR:  ogip_check returned an error status!"
       let errors+=1
    fi
    out="$(diff ref/${file}.ogip_check.log out/${file}.ogip_check.log)"
    #  Bizarre bash way to split output by newlines into array in $diffs
    IFS=$'\n' read -rd '' -a diffs <<< "$out"

    #  Don't print all of it if it's long:
    if [[ ${#diffs[@]} != 0 ]]; then
	if [[ ${#diffs[@]} -lt 5 ]]; then
	    echo "ERROR:  Differences appear:"
	    for ln in ${diffs[@]} ; do echo "$ln"; done
	else
	    echo "################"
	    echo "ERROR:  Differences appear;  showing last 5 lines of diff:"
	    let start=${#diffs[@]}-5
	    for (( i=${start};i<${#diffs[@]};++i )); do echo -e "${diffs[i]}"; done
	    echo "################"
	fi
	let errors+=1
    else
	echo "No differences."
    fi
done
echo ""

echo "##################################################################"
echo "#  Run by specifying the type:"

# TIMING EVENT
echo ""
file="timing.evt"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t TIMING>& out/${file}.ogip_check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diffs=`diff ref/${file}.ogip_check.log out/${file}.ogip_check.log`
if [[ ${#diffs} != 0 ]]; then
    echo "ERROR:  Differences appear, for example:"
    echo diffs | tail
    let errors+=1
else
    echo "No differences."
fi
echo ""

# TIMING Light curve
echo ""
file="timing_passes.lc"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t TIMING >& out/${file}.ogip_check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log2 out/${file}.ogip_check.log2 | tail
echo ""

# SPECTRAL
echo ""
file="spectrum.pha"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t SPECTRAL >& out/${file}.ogip_check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log2 out/${file}.ogip_check.log2 | tail
echo ""
    
# RMF
echo ""
file="specresp_matrix.rmf"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t RMF >& out/${file}.ogip_check.log2
retval=$?
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log2 out/${file}.ogip_check.log2 | tail
echo ""

# ARF
echo ""
file="hexte.arf"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t ARF >& out/${file}.ogip_check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log2 out/${file}.ogip_check.log2 | tail
echo ""

# CALFILE
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t CALDB >& out/${file}.ogip_check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log2 out/${file}.ogip_check.log2 | tail
echo ""




echo "##################################################################"
echo "#  Some error cases"

# Test giving invalid type
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file} with bad type"g
../ogip_check inputs/${file} -t BLAH >& out/bad_type.ogip_check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/bad_type.ogip_check.log out/bad_type.ogip_check.log | tail
echo ""


# Test giving wrong type
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file} with incorrect type"
../ogip_check inputs/${file} -t TIMING >& out/wrong_type.ogip_check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/wrong_type.ogip_check.log out/wrong_type.ogip_check.log | tail
echo ""


# Test giving missing file
echo ""
file="missing.fits"
echo "Checking file ${file}"
../ogip_check inputs/${file} >& out/${file}.ogip_check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  You should see nothing."
diff ref/${file}.ogip_check.log out/${file}.ogip_check.log | tail
echo ""







#  Summarize test results
echo ""
echo "##################################################################"
if [[ $errors -eq 0 ]]; then 
    echo "#  Test completed with $errors errors"
else
    echo "#  ERROR:   Test completed with $errors errors"
fi
echo ""

exit $errors
