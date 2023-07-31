# Just some thoughts.

##### Still need to come up with some sort of persistence storage strategy to either save the individual scripts or chats.

-------

### Caching
To incorporate this we'd just need to write to continuously save to this 
file before returning the script-- we could even just run the script once 
this file has been updated. 

    This would be sort of a textEditor-IDE merge.

# A simple example I had earlier
##### I saved only the code~:

```python
import numpy as np
import matplotlib.pyplot as plt

# Generate some random data to plot
data = np.random.normal(0, 10, size=(100,))

# Plot the histogram
plt.hist(data, bins=20, alpha=0.5, label='Random Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.show()
```
-------
# Alternatively

We could actually implement a storage system that lets you save each generated
scripts (along with its iterations and refactors), along the explanation-- wrapped 
as python comments.

# Moreover
It's should be possible (?) to even have an option to sys instruct the model to and have
it output its response in a JupyterNotebook fashion.
    
    Basically have auto-generated guides.

 