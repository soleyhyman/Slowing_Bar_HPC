# Slowing_Bar_HPC
Slowing Bar Integration for HPC
This program integrates a numpy array (.npy file) of cylindrical cords, returning 3 numpy arrays of cylindrical, cartesian, and action potential values. 
### THIS PROGRAM MUST BE RUN ON A HPC ###
# Instructions
To run this program first open terminal 
1. ssh USERNAME@hpc.arizona
2. Navigate to where you want to download the program. Using cd to navigate.
3. In the terminal enter: git clone https://github.com/ezpasss/Slowing_Bar_HPC.git
Once this is completed the Slowing Bar Integration is downloaded.
# Running the program
Use cd to navigate into the parent directory --> cd Slowing_Bar_HPC/
Once here, move the input file into the !_Input folder.
The files can be moved in two ways. 
  Using the HPC OnDemand
  1. Using the HPC OnDemand navigate to the !_Input folder and click upload.
  2. Either drag the input npy file to the submission box or browse your files and select it.
  Using the file transfer system. 
  1. USING A SEPARATE TERMINAL first navigate to the local directory where the input file is located.
  2. Connecting to the HPC's file transfer service in terminal using --> sftp USERNAME@filexfer.hpc.arizona.edu
  3. You are now on the HPC, navigate to the !_Input folder using cd in terminal.
  4. In Terminal use put (FILENAME)
# Modifying the program for your use
For the program to run properly you must modify some lines in slowing_bar_run_hpc.sh
This can be achieved using the HPC's OnDemand or through the terminal. 
  # Through Terminal
  1.   Navigate to the program's parent directory.
  2.   In the terminal enter nano slowing_bar_run_hpc.sh
