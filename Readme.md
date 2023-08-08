Group01 : FW Update case:

    16990 JXDU:Disconnect the DUT during the FW update.[Use JX Package][Allow downgrade]
    16991 JXDU:Disconnect the DUT during the FW udpate.[Use JX Package][Not allow downgrade]
    16992 JXDU:Disconnect the DUT during the FW update,for all individual components.[Use FW File]
    17950 JXDU:Normal FW update without Interruption.[Use FW File](Linux JXDU 6.x or above)
    17951 JXDU:Normal FW Update without Interruption.[Use JX Package](Linux JXDU 6.x or Above)

Group02 :FW Update & Settings Configure case:
    
    6098 JX-ThinC: Verify zip package content and JXDU version by creating a ZIP file. - - It is a check test case, not need tu run code so dont need another prepare pakcage for this.
    6134 JX-ThinC:All device settings and FW set to "Leave Unchange",all settings set to Protected.
    7692 JX-ThinC:All settings in the device can be change from default value to min.value with installation of .zip file at the end user PC,no FW change.
    7695 JX-ThinC:All settings in the device can be change from default value to max.value with installation of .zip file at the end user PC,no FW change.
    7551 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.
    7555 JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.
    7556 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.

Group03 :Prepare package for 01:

    16990p: Lower FW and not settings change,downgrade==allow.
    16991p: same with 16990p
    16992p: same with 16990p
    17950p: same with 16990p
    17951p: same with 16990p

Group04 :Prepare testcase for 02:

    6134p: Latest FW and Random settings, Protect = Not.
    7692p: Use the pacakge == 7556.
    7695p: Use the pacakge == 7556.
    7551p: Lower FW and Random settigns.
    7555p: Lower FW and settings = Max value.
    7556p: Lower FW and not default settings.
