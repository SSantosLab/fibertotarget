This folder has the codes for the FTA. Each piece of code is commented throughout, but here is a brief explanation about how to use it. 

Prep the Data!
GC_data.py - Galaxy cluster data, pick a cluster and assign priorities
RSS_data.py - Redshift Survey data, pick a sky area (and/or magnitude) and assign prioirites
overlapdata.py - You might want to use the data sets prepared above together. Use this code to prepare a data set with both target types and their info. 

Run the code!
sim.py - This is the main simulated annealing schedule

Test these files!
tx --> *_test_x.txt
ty --> *_test_y.txt
prior--> *_targetgalaxytestprior.txt (lol these names are so bad, sorry about that)
info --> *_targetinfo.txt

* can be GC, RSS, or OV. You can play around with the different data sets making sure that you only use the same type of data set for all values (GC with GC, and so on). The output graphs should be comparable to the graphs (also labeled with GC, RSS, or OV) in the graphs folder. They will not be identical, because the code will not come to the exact same solution everytime. Run it a few times and make sure the all the runs produce similar results. 

Note: fiberloc.py
This code has a function used by the sim.py. You can mess around with the fiber arrangement here if you want. Currently, we arrange them in a checkerboard pattern according to the pitch. 