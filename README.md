# aurora_core
A Python Library Controls  [Nanoleaf Light Panels (formerly Aurora)](https://nanoleaf.me/en/consumer-led-lighting/products/smarter-series/nanoleaf-light-panels-smarter-kit/)

## Usage
- The libaray contains three main classes: `Discover`, `Manager`, and `Aurora`. After getting an `Aurora` instance, the usage should be straightforward:

```Python
aurora.get.name()				#return the name of the panel cluster
aurora.set.on(False)				#turn off the panel cluster
aurora.set.effect('Rainfall')			#set effect to "Rainfall"
```

- To get an `Aurora` instance, the easiest way is using the `Discover` class:

```Python
from aurora_core import Discover

def authed_handler(aurora):			#the callback function once a new aurora got authed
	print aurora.get.name(), aurora.get.serial()
	aurora.set.brightness(50)
	
discover = Discover([], authed_handler)		#[] is all auroras need to be ignored
discover.start()
```

You have to **hold the power button for ~5 seconds** to give this script permission to access the Light Panels. This script will set the cluster brightness to 50% after finishing authorization.

- Apparently no one want to authenticate/permit access everytime. `Manager` provides basic `Aurora` object management, including data persistence:

```Python
from aurora_core import Manager
manager = Manager('example_db')			#local data store at `example_db`

for aurora in manager.auroras():		#print out all local aurora names
	print aurora.get.name()
manager.save(new_aurora)			#save new_aurora to local
manager.delete(new_aurora)			#delete new_aurora from local
```

Please note that the `Manager` is using `pickle` internally, so no encryption will be applied on the local storage.
