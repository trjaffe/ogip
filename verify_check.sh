#!/bin/bash
echo "checking $@"

for file in $( find $@ -name \*.log -print );
do

    awk '/Card '\''/{print $4}' $file | awk -F\' '{print $2}' > ${file}.pyverify_keywords
    [ ! -s ${file}.pyverify_keywords ] && rm ${file}.pyverify_keywords

    awk '/Keyword/{print $6}' $file | awk -F: '{print $1}' > ${file}.ftverify_keywords
    [ ! -s ${file}.ftverify_keywords ] && rm ${file}.ftverify_keywords

    if  [[ ! -e ${file}.pyverify_keywords && ! -e ${file}.ftverify_keywords ]]; then
	continue
    elif [[ -e ${file}.pyverify_keywords && ! -e ${file}.ftverify_keywords ]]; then
	echo "WARNING:  For file ${file}, found pyverify output but no ftverify output"
	continue 
    elif  [[ -e ${file}.ftverify_keywords && ! -e ${file}.pyverify_keywords ]]; then
	echo "WARNING:  For file ${file}, found ftverify output but no pyverify output"
	continue 
    fi
#	echo "For file ${file}, found both ftverify output and pyverify output."
#	echo "Comparing into ${file}.verify_diff"  
#    fi

    diff ${file}.ftverify_keywords ${file}.pyverify_keywords > ${file}.verify_diff
    if [ ! -s ${file}.verify_diff ]; then
	rm ${file}.verify_diff 
    else
	echo "WARNING:  for file ${file}, found differences between ftverify and pyverify keywords."
    fi

done

 
