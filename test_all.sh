#!/bin/bash
# test_all.sh
#
# Run this on a CSCE linux lab machine from the directory where you
# unzipped prog-proj4.zip, after placing my_interpreter.py in that
# same directory.
#
# This replicates what the grading script does:
#   1. Run your interpreter on each test case
#   2. Run the reference ./2ca on each test case
#   3. Strip whitespace with sw.pl (or sed as a fallback)
#   4. Diff the two outputs
#
# If a test passes, you see "PASS". If it fails, you see the diff.

# List of test files and their point values
declare -A POINTS
POINTS[ab]=15
POINTS[abc]=15
POINTS[abcd]=15
POINTS[equal01]=15
POINTS[match_delim1]=15
POINTS[semibalanced]=15
POINTS[match_delim2]=20

TOTAL=0
POSSIBLE=0

for name in ab abc abcd equal01 match_delim1 semibalanced match_delim2; do
    txt="${name}.txt"
    inp="${name}.in"
    pts=${POINTS[$name]}
    POSSIBLE=$((POSSIBLE + pts))

    # Check that the test files exist
    if [ ! -f "$txt" ] || [ ! -f "$inp" ]; then
        echo "[$name] SKIP - missing $txt or $inp"
        continue
    fi

    # Run your interpreter with an 11-second timeout (matches grading script)
    timeout 11 python3 my_interpreter.py "$txt" < "$inp" | sed 's/[ \t\r]//g' > /tmp/my_out_${name}.txt 2>/dev/null

    # Run the reference solution
    timeout 11 /lib64/ld-linux-x86-64.so.2 ./2ca "$txt" < "$inp" | sed 's/[ \t\r]//g' > /tmp/ref_out_${name}.txt 2>/dev/null

    # Compare
    if diff -q /tmp/my_out_${name}.txt /tmp/ref_out_${name}.txt > /dev/null 2>&1; then
        echo "[$name] PASS  (+${pts} pts)"
        TOTAL=$((TOTAL + pts))
    else
        echo "[$name] FAIL  (+0 pts)"
        echo "  First few differences:"
        diff /tmp/my_out_${name}.txt /tmp/ref_out_${name}.txt | head -20
        echo ""
    fi
done

# Cap at 100
if [ $TOTAL -gt 100 ]; then
    TOTAL=100
fi

echo ""
echo "Score: ${TOTAL} / 100"
