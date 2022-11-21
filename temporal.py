import tempfile
import time

import shutil

#with tempfile.TemporaryDirectory() as tmpdirname:


tmpdirname = tempfile.TemporaryDirectory()
print('created temporary directory', tmpdirname)

print("Muevo imagen")
shutil.copy("C:\\Users\\David de la Rosa\\Aimagenes\\L1__2017-06-15__08-58-45(1)__empty.JPG", str(tmpdirname.name))
time.sleep(120)