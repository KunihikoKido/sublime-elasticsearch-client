import os
import sys
from imp import reload

package_path = os.path.dirname(__file__)
libpath = os.path.join(package_path, "lib")

if libpath not in sys.path:
    sys.path.append(libpath)


for module in sys.modules:
    if module.startswith("ElasticsearchClient.commands."):
        print("reloading plugin {}".format(module))
        reload(sys.modules[module])

module = "ElasticsearchClient.commands"
if module in sys.modules.keys():
    print("reloading plugin {}".format(module))
    reload(sys.modules[module])

from .commands import *
