#!/bin/bash

# Make sure you've run the programmer from Quartus and have Quartus 18.1 installed - if not then change 
# the number in the command below to the appropriate version

# May need to run this in powershell in admin mode: powershell -command "Set-ExecutionPolicy Unrestricted"

cd ..
cd ..
& '.\intelFPGA_lite\18.1\nios2eds\Nios II Command Shell.bat' ./E2_CAS/SpaceSurfer/output_inputs.sh
cd E2_CAS/SpaceSurfer