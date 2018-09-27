SYSTEM INFORMATION:
Python Version: 2.7.10
Computer: MacBook Pro Early 2015
IDE: Visual Studio Code with Microsoft Python Extension
Operating System: macOS Mojave version 10.14


HOW TO RUN PROGRAM:
To run the program, type the following in the command line:
python puzzlesolver.py XXX.config YYY ZZZ

XXX = name of the config file
YYY = algorithm name. Can be one of the following: "bfs", "dfs", "unicost", "greedy", "astar"
ZZZ = optional heuristic, to be used for greedy and astar algorithms. Can be one of the following values: 
	For water jugs          --> "proximity"
	For path finding cities -->"euclidean"
	For tiles 		        --> "misplaced" or "manhattan"

Example runs:
To run the cities puzzle with the Euclidean heuristic and astar algorithm, type:
python puzzlesolver.py test_cities.config astar euclidean

To run the jugs puzzle with unicost, type:
python puzzlesolver.py test_jugs.config unicost


ADDITIONAL RESOURCES/DISCUSSIONS:
No outside sources other than class notes, the textbook, and the Python 2 documentation (https://docs.python.org/2/contents.html) were used. 
I discussed string/tuple/state/board/path representation with Hassan Syed.


OTHER:
There are no known bugs in the program and all components of program work as per the project specifications.



