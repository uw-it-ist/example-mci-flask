# need to monkey patch to make things work with eventlet and monkey patching
# needs to happen super early in the loading of the system. by doing it here it
# happens before any code is really run.
import tools.monkey
tools.monkey.patch()

# then load the program normally
from .app import load  # noqa: F402
app = load()
