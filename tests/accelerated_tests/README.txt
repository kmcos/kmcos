The accelerated feature **requires** paired reactions: for each reaction added, the next reaction is the 'opposite' reaction.  

To run the test I use a model for CO oxidation including the JANAF dependency.
From previous work I know that for certain T,pCO,pO2 parameters the expected speedup from the acceleration algorithm is about a factor of 10.
The three different .py files all implement this same model. The only difference is the model name, which, when the model is exported, becomes the name of the folder where each of 3 different tests are carried out.
The three tests seem to work as expected.
To run the tests I used the snapshots module with the implementation allowing to run acc steps.
The runfiles and output CSV files can be found in each folder.
First, I ran the model without the acceleration backend. Here I needed 3E6 steps in each of the 10 snapshots in order to get a sufficient sampling of the TOF in each snapshot (otherwise some snapshots gave 0 TOF)
Then I ran the model with the acceleration backend, but using do_steps. As expected, the output is identical to before.
Finally, I ran the model using the acceleration backend and do_acc_steps. Here I could get away with 3E5 steps in each snapshot. The output looks rather similar, but is of course not completely identical.


Example non accelerated output (around 1 minute of running)
['CO_ruo2_bridge', 'CO_ruo2_cus', 'O_ruo2_bridge', 'O_ruo2_cus', 'empty_ruo2_bridge', 'empty_ruo2_cus']
[5.213017043523873e-07]
[[1.0, 0.9975], [0.0, 0.0], [0.0, 0.0025]]

Example non accelerated output after compiling with acc backend (around 1 minute of running)
['CO_ruo2_bridge', 'CO_ruo2_cus', 'O_ruo2_bridge', 'O_ruo2_cus', 'empty_ruo2_bridge', 'empty_ruo2_cus']
[5.213017043523873e-07]
[[1.0, 0.9975], [0.0, 0.0], [0.0, 0.0025]]


Example accelerated output after compling with acc backend (around 5 seconds of running)
['CO_ruo2_bridge', 'CO_ruo2_cus', 'O_ruo2_bridge', 'O_ruo2_cus', 'empty_ruo2_bridge', 'empty_ruo2_cus']
[3.421010622253541e-07]
[[1.0, 0.9975], [0.0, 0.0], [0.0, 0.0025]]




