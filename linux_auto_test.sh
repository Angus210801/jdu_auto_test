#!/bin/bash

# Ask user the which Test RC and what the device test.
echo "Please enter the Test RC number(like sr40db1): "
read rc

echo "Please enter the device test(like Engage75): "
read device

# Set the address for the test RC and device, the test address is https:192.168.140.95+rc+device
test_address="http://192.168.140.95/xpress/$rc/$device"

# Keep the test result file name as "autotest_log.txt" under the /tmp directory.
# If the file exists, delete it,otherwise create it.
if [ -f /tmp/autotest_log.txt ]; then
    rm -rf /tmp/autotest_log.txt
fi
touch /tmp/autotest_log.txt

# Output the test address to the log file.
echo "The test address is: $test_address" >> /tmp/autotest_log.txt

# Cut in to the /usr/loacl/gn directory.
cd /usr/local/gn

# Make a function that run the ./jdu_settings -c -V $xpress_package_file command.
function jdu_settings_compare() {
    xpress_package_file=$(find /var/run/jabra/ -name 'xpress_package_2*')
    ./jdu_settings -c -V $xpress_package_file
}

# Use the wget command to get the lowerfw.zip from test_address/lowerfw.zip. Before run the command, make sure the lowerfw.zip is not exist under the /tmp directory.
if [ -f /tmp/lowerfw.zip ]; then
    rm -rf /tmp/lowerfw.zip
fi
echo "$test_address/lowerfw.zip"
/usr/bin/wget -P /tmp/ "$test_address/lowerfw.zip"
wait

# testcase group 01 contains thost test case need FW update.
# testcase group 02 contains thost test case only settings update.
# testcase group 03 contains thost test case need FW update and settings update.
testcase_group01=(16990 16991)
testcase_group02=(6134 7692 7695)
testcase_group03=(7551 7555 7556)
# Start the loop to run the test case.

# Run the test case in the testcase_group01. Use the ./jfwu /tmp/lowerfw.zip to update the FW. Then use the ./jdu.sh $test_address/$i to run the test case.
for i in ${testcase_group01[@]}
do
    # Output the test case name to the log file.
    echo "The test case name is: $i" >> /tmp/autotest_log.txt
    # Run the test case.
    test_adderss=test_address/$i
    echo "The test address is: $test_address/$i" >> /tmp/autotest_log.txt

    ./jfwu /tmp/lowerfw.zip >> /tmp/autotest_log.txt
    wait
    echo "The device is downgrade to lower FW, next, run the test case." >> /tmp/autotest_log.txt

    ./jdu.sh $test_address/$i >> /tmp/autotest_log.txt
    wait
    echo "The test case run done." >> /tmp/autotest_log.txt

    # Make a split line to separate the test case.
    echo "----------------------------------------" >> /tmp/autotest_log.txt
    # Move to next line.
    echo "" >> /tmp/autotest_log.txt
    sleep 30s
done

for i in ${testcase_group02[@]}
do
    # Output the test case name to the log file.
    echo "The test case name is: $i" >> /tmp/autotest_log.txt
    # Run the test case.
    test_adderss=test_address/$i
    echo "The prepare test case address is: $test_address/$i"p"" >> /tmp/autotest_log.txt
    echo "The test case address is: $test_address/$i" >> /tmp/autotest_log.txt

    ./jdu.sh $test_address/$i"p" >> /tmp/autotest_log.txt
    wait
    echo "The device is update to the pre-condition, next, compare the device settings with the pre-condition package." >> /tmp/autotest_log.txt

    jdu_settings_compare >> /tmp/autotest_log.txt
    wait
    echo "The compare action done, start to run the test case." >> /tmp/autotest_log.txt

    ./jdu.sh $test_address/$i >> /tmp/autotest_log.txt
    wait
    echo "The test case run done." >> /tmp/autotest_log.txt

    jdu_settings_compare >> /tmp/autotest_log.txt
    wait
    echo "The test case settings compare done." >> /tmp/autotest_log.txt
    echo "----------------------------------------" >> /tmp/autotest_log.txt
    # Move to next line.
    echo "" >> /tmp/autotest_log.txt
    sleep 30s
done

for i in ${testcase_group03[@]} 
do
    # Output the test case name to the log file.
    echo "The test case name is: $i" >> /tmp/autotest_log.txt
    # Run the test case.
    test_adderss=test_address/$i
    echo "The prepare test case address is: $test_address/$i"p"" >> /tmp/autotest_log.txt
    echo "The test case address is: $test_address/$i" >> /tmp/autotest_log.txt

    ./jfwu /tmp/lowerfw.zip >> /tmp/autotest_log.txt
    wait
    echo "The device is downgrade to lower FW, next, run the test case." >> /tmp/autotest_log.txt


    ./jdu.sh $test_address/$i"p" >> /tmp/autotest_log.txt
    wait
    echo "The device is update to the pre-condition, next, compare the device settings with the pre-condition package." >> /tmp/autotest_log.txt

    jdu_settings_compare >> /tmp/autotest_log.txt
    wait
    echo "The compare action done, start to run the test case." >> /tmp/autotest_log.txt

    ./jdu.sh $test_address/$i >> /tmp/autotest_log.txt
    wait
    echo "The test case run done." >> /tmp/autotest_log.txt

    jdu_settings_compare >> /tmp/autotest_log.txt
    wait
    echo "The test case settings compare done." >> /tmp/autotest_log.txt
    echo "----------------------------------------" >> /tmp/autotest_log.txt
    # Move to next line.
    echo "" >> /tmp/autotest_log.txt
    sleep 30s
done

# Rename the log to autotest+devicename+date.txt.
mv /tmp/autotest_log.txt /tmp/autotest_$device_name_$(date +%Y%m%d).txt
