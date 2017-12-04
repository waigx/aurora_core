# aurora_core
A Python Library Controls  [Nanoleaf Light Panels (formerly Aurora)](https://nanoleaf.me/en/consumer-led-lighting/products/smarter-series/nanoleaf-light-panels-smarter-kit/)

## Usage
The libaray contains three main classes: `Discover`, `Manager`, and `Aurora`. After getting an `Aurora` instance, the usage should be straightforward:

```Python
aur.get.name()				#return the name of the panel cluster
aur.set.on(False)			#turn off the panel cluster
aur.set.brightness(80)		#set brightness to 80%
aur.set.effect('Rainfall')	#set effect to "Rainfall"
```

To get an `Aurora` instance, the easiest way is using the `Discover` class:

```Python
from aurora_core import Discover

def authed_handler(aurora):
	print aurora.get.name(), aurora.get.serial()
	aurora.set.brightness(50)
	
discover = Discover([], authed_handler)
discover.start()
```

You have to **hold the power button for ~5 seconds** to give this script permission to access the Light Panels. This script will set the cluster brightness to 50% after finishing authorization.
