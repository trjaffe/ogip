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


if [[ -e out ]]; then rm -r out
fi
mkdir out

let errors=0
let diffcnt=0

echo "##################################################################"
echo "# Basic tests, i.e., run each file type with no arguments:"
for file in $( ls inputs );
do
#    echo "got file=${file}."
    if [ -d "inputs/${file}" ]; then 
	continue
    fi
    echo ""
    echo "Checking file ${file}"
    ../ogip_check inputs/${file} &> out/${file}.check.log
    retval=$?
    echo "Return status was $retval"
    if [[ "$retval" != "0" ]];  then
       echo "ERROR:  ogip_check returned an error status!"
       let errors+=1
    fi

    diffs=`diff -I logfile ref/${file}.check.log out/${file}.check.log`

    if [[ ${#diffs} != 0 ]]; then 
	echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log out/${file}.check.log'"
	let diffcnt+=1
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
../ogip_check inputs/${file} -t TIMING>& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""

# TIMING Light curve
echo ""
file="timing_passes.lc"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t TIMING >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""

# SPECTRAL
echo ""
file="spectrum.pha"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t SPECTRAL >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""

# SPECTRAL
echo ""
file="spectrumII.pha"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t SPECTRAL >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""



    
# RMF
echo ""
file="specresp_matrix.rmf"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t RMF >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""

# ARF
echo ""
file="hexte.arf"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t ARF >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""

# CALFILE
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file}"
../ogip_check inputs/${file} -t CALDB >& out/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log2 out/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log2 out/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""




echo "##################################################################"
echo "#  Some error cases"

# Test giving invalid type
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file} with bad type"
../ogip_check inputs/${file} -t BLAH >& out/bad_type.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/bad_type.check.log out/bad_type.check.log`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/bad_type.check.log out/bad_type.check.log'"
    echo $diffs
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""


# Test giving wrong type
echo ""
file="fermi_lat_bcf_edisp_calfile.fits"
echo "Checking file ${file} with incorrect type"
../ogip_check inputs/${file} -t TIMING >& out/wrong_type.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/wrong_type.check.log out/wrong_type.check.log`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/wrong_type.check.log out/wrong_type.check.log'"
#    echo ${diffs[@]}
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""


# Test giving missing file
echo ""
file="missing.fits"
echo "Checking file ${file}"
../ogip_check inputs/${file} >& out/${file}.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" == "1" ]]; then 
    echo "(This is the expected status for this error case.)"
else 
    echo "ERROR:  Return status is ${retval};  expected 1"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/${file}.check.log out/${file}.check.log`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/${file}.check.log out/${file}.check.log'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""







#  Test the directory tool
echo ""
echo "##################################################################"
echo "Checking entire contents of directory inputs"
mkdir out/inputs.logs
../ogip_check_dir inputs out/inputs.logs --default_type 'CALDB' -v 2 >& out/inputs.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check_dir returned an error status!"
    let errors+=1
else
    echo "Comparing output to reference.  "
    diffs=`diff  -I TIMESTAMP -I logfile ref/inputs.check.log out/inputs.check.log`
    if [[ ${#diffs} != 0 ]]; then
	echo "WARNING:  Differences appear in 'diff -I TIMESTAMP -I logfile ref/inputs.check.log out/inputs.check.log'"
	#    echo ${diffs[@]} | tail
	let diffcnt+=1
    else
	echo "No differences in directory check log."
    fi
    echo "Comparing logs of individual files run this way with those run individually."
    for file in asca_sis_bcf_calfile.fits fermi_lat_bcf_edisp_calfile.fits hexte.arf specresp_matrix.rmf spectrum.pha spectrumII.pha timing.evt timing_fails.lc timing_passes.lc ; do 
	diffs=`diff -I TIMESTAMP -I dtype -I logfile out/${file}.check.log out/inputs.logs/${file}.check.log`
	if [[ ${#diffs} != 0 ]]; then
	    echo "WARNING:  Differences appear in 'diff -I TIMESTAMP -I dtype -I logfile out/${file}.check.log out/inputs.logs/${file}.check.log'"
	    let diffcnt+=1
	fi
    done
    echo "Comparing logs of individual files run this way against ref."
    for file in $( (cd out;  find inputs.logs ) );
    do
	if [ -d out/${file} ]; then
	    continue
	fi
	diffs=`diff ref/${file} out/${file}`
	if [[ ${#diffs} != 0 ]]; then
	    echo "WARNING:  Differences appear in 'diff ref/${file} out/${file}'"
	    let diffcnt+=1
	fi
    done

fi

echo ""
echo ""
echo "Checking without using CALDB as default for unknown types:"
mkdir out/inputs2.logs
../ogip_check_dir inputs out/inputs2.logs -v 2 >& out/inputs2.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check_dir returned an error status!"
    let errors+=1
else
    echo "Comparing output to reference.  "
    diffs=`diff -I TIMESTAMP -I logfile ref/inputs2.check.log out/inputs2.check.log`
    if [[ ${#diffs} != 0 ]]; then
	echo "WARNING:  Differences appear in 'diff -I TIMESTAMP -I logfile ref/inputs2.check.log out/inputs2.check.log'"
	#    echo ${diffs[@]} | tail
	let diffcnt+=1
    else
	echo "No differences in directory check log."
    fi
fi




#  Test the directory tool
echo ""
echo "##################################################################"
echo "Checking entire contents of directory inputs with rxte ignores"
../ogip_check_dir inputs out/inputs3.logs --meta_key rxte -v 2 >& out/inputs3.check.log
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check_dir returned an error status!"
    let errors+=1
else
    echo "Comparing output to reference.  "
    diffs=`diff  -I TIMESTAMP -I logfile ref/inputs3.check.log out/inputs3.check.log`
    if [[ ${#diffs} != 0 ]]; then
	echo "WARNING:  Differences appear in 'diff -I TIMESTAMP -I logfile ref/inputs3.check.log out/inputs3.check.log'"
	#    echo ${diffs[@]} | tail
	let diffcnt+=1
    else
	echo "No differences in directory check log."
    fi
fi





echo ""
echo "##################################################################"
echo "#  Re-checking a single file with meta-data to supersede certain requirements:"
echo ""
file="chandra/hrcf00025N005_pha2.fits.gz"
echo "Checking file ${file}"
../ogip_check inputs/${file} --meta_key=chandra >& out/inputs.logs/${file}.check.log2
retval=$?
echo "Return status was $retval"
if [[ "$retval" != "0" ]]; then 
    echo "ERROR:  ogip_check returned an error status!"
    let errors+=1
fi
echo "Comparing output to reference.  "
diffs=`diff -I logfile ref/inputs.logs/${file}.check.log2 out/inputs.logs/${file}.check.log2`
if [[ ${#diffs} != 0 ]]; then
    echo "WARNING:  Differences appear in 'diff -I logfile ref/inputs.logs/${file}.check.log2 out/inputs.logs/${file}.check.log2'"
#    echo ${diffs[@]} | tail
    let diffcnt+=1
else
    echo "No differences."
fi
echo ""






#  Summarize test results
echo ""
echo "##################################################################"
if [[ $errors == 0 && $diffcnt == 0 ]]; then 
    echo "#  Test completed with $errors errors and $diffcnt differences"
else
    echo "#  ERROR:   Test completed with $errors errors and $diffcnt differences"
fi
echo ""

exit $errors
