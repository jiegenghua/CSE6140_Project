BnB.py: the branch and bound algorithm \
HC.py: the hill climbing algorithm \
SA.py: the simulated annealing algorithm \
FPTAS.py: approximate algorithm based on dynamic programming \
main_KSP.py: the main function

To run the code:
```angular2html
Python main_KSP.py -inst filename -alg "[BnB|FPTAS|HC|SA]" -time "cutoff time" -seed 1
```
For example, you can run the small-1 instance by the following command:
```angular2html
Python main_KSP.py -inst .\\DATA\\DATASET\\small_scale\\small_1 -alg HC -time 5 -seed 1
```
The results (solution files and trace files) are saved in the folder "output" named by the name of the instances.

To plot the QRTD plot and SQD plot for the large-scale 1 and large-scale 3 instances with 
results of using the Simulated annealing and Hill climbing algorithm,
change the flag ```LS_plot``` in the ```main_KSP.py```to be true.
Make sure the trace files for 20 or more runs are stored in a folder.

A detailed report can be folder in the same folder, named as ```report.pdf```.