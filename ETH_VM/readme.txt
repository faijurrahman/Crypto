Install py-evm before running the test with command:
python3 -m pip install py-evm
OR
Get the package source code from here: git clone --recursive https://github.com/ethereum/py-evm.git




If the project is run in Windows Machine, there might be an error for pyethash package.
Fix for the package:
Step 1:
Clone the project from github
git clone https://github.com/ethereum/ethash

Step 2:
he version you get when cloning the project from the git is 1.23 and the latest version is 1.27.
I fixed this by adding all the files from the latest update manually.
http://archive.linux.duke.edu/pypi/simple/pyethash/
This solved the problem you both are experiencing for me.

Step 3:
Open <PATH_TO_ETHASH_LIBRARY>\src\libethash\mmap_win32.c for editing

Step 4:
Add the following after the last #include statement
#pragma comment(lib, "Shell32.lib")

Step 5:
Open <PATH_TO_ETHASH_LIBRARY>\src\python\core.c

Step 6:
Replace:
#include <alloca.h>
with:
#if defined(_WIN32) || defined(WIN32)
#include <malloc.h>
#else
#include <alloca.h>
#endif

Step 7:
Run the following in the source code main folder
python3 setup.py build
python3 setup.py install
