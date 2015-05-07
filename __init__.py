import os
import sys

package_path = os.path.dirname(__file__)
libpath = os.path.join(package_path, "lib")

if libpath not in sys.path:
    sys.path.append(libpath)
