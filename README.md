Code Running:

Firstly, to be able to dissociate this project from your other python projects, it is
advisable to use a new virtual environment using these commands :

1. python3.11 -m venv /path/to/new/virtual/environment/name of env
2. source /path/to/new/virtual/environment/name of env/bin/activate
   
Secondly, in order to run the code without errors, you must install the packages located in
requirements.txt using the pip install command. Finally, you can run the main.py
file in the src folder.

Interface Explanation: 

Once the code is launched, the user can walk around the map of Brussels, zooming
in and clicking on buttons. They can click on the nodes as many times as they like. To
launch the Physarum and Dijkstra algorithms. The user has the choice of either selecting
the 2 nodes he wants himself or pressing the button on the right ”2random nodes” so
that it selects 2 random nodes. Once the nodes have been selected, the user can run the
physarum agorithm. When the user presses the ”Physarum” button, a pop-up window
appears asking how many step algorithms he wants. Once selected, the algorithm is
launched. The results of the shortest path will be displayed in red between the 2 nodes.
If the user wants to run the Dijkstra agorithm, simply press the Dijkstra button. The
result of the shortest path will appear in blue. If the user wants to see the details of these
runs, they can go to the following file: experiments/results.csv. Finally the user has the
choice to start running the algorithms again by pressing the clear button and choosing 2
other nodes to test.

