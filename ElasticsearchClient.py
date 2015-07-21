import os
import sys
from imp import reload

package_path = os.path.dirname(__file__)
libpath = os.path.join(package_path, "lib")

if libpath not in sys.path:
    sys.path.append(libpath)


def reload_modeule(module):
    print("reloading plugin {}".format(module))
    reload(sys.modules[module])


for module in sys.modules:
    if module.startswith("ElasticsearchClient.panel."):
        reload_modeule(module)

module = "ElasticsearchClient.panel"
if module in sys.modules.keys():
    reload_modeule(module)

for module in sys.modules:
    if module.startswith("ElasticsearchClient.commands."):
        reload_modeule(module)

module = "ElasticsearchClient.commands"
if module in sys.modules.keys():
    reload_modeule(module)

from .commands import *
