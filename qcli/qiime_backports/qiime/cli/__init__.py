import os
import glob

# from http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")
                             if not os.path.basename(f).startswith('__init__')]
__all_lookup__ = set(__all__)

