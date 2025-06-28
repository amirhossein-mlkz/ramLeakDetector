#  RamLeakDetector
A lightweight memory leak monitoring tool for Python applications.

## Step 1: Initialization
In your application, create an instance of the `RamLeakDetector` class:

```python

detector = RamLeakDetector()

```
## Step 2: Start Your Application

Run your software normally and allow it to complete its initial execution loop, so memory is occupied as usual.

## Step 3: Start Monitoring
Once the application is stable:
Press `Ctrl + Alt + S` to \*\*start memory monitoring\*\*.
A folder will be created at:

```
<project\_directory>/ramLeak.logs/RamLeakRecorder
```
The session folder will be named:
```
RamLeakDe\_<current-date>\_<current-time>
```
Memory snapshots are taken \*\*every 30 seconds by default\*\*.
  
## Step 4: Let the App Run
Let the application run under realistic usage to allow memory leaks to develop.  
We recommend at least \*\*10 minutes\*\* of runtime.

## Step 5: Export Memory History
When you suspect a memory leak has occurred:
Press `Ctrl + Alt + E` to \*\*export the memory history\*\*.
A file named `history.hist` will be generated in the session folder.

## Step 6: Generate Plots and Report
To visualize and analyze the memory data:
Press `Ctrl + Alt + P` to generate output:
A `plots` subfolder will be created, containing memory usage graphs sorted by growth rate.
`report.txt` file will be generated, summarizing findings and highlighting leak-prone areas.


## Summary of Shortcuts 
| Shortcut         | Action                          |
|------------------|---------------------------------|
| `Ctrl + Alt + S` | Start monitoring                |
| `Ctrl + Alt + E` | Export memory history (`.hist`) |
| `Ctrl + Alt + P` | Generate plots and report       |

## Output Folder Structure
```
ramLeak.logs/

└── RamLeakRecorder/
# &nbsp;   └── RamLeakDe\_YYYY-MM-DD\_HH-MM-SS/

# &nbsp;       ├── history.hist

# &nbsp;       ├── report.txt

# &nbsp;       └── plots/

# &nbsp;           ├── plot\_1.png

# &nbsp;           ├── plot\_2.png

# &nbsp;           └── ...

# ```

# 

# ---

# 

# \## 🔧 Configuration

# 

# \- Default snapshot interval: \*\*30 seconds\*\*

# \- Customization options coming soon!

# 

# ---

# 

# \## 🛠 Requirements

# 

# \- Python 3.7 or higher

# \- `psutil`

# \- `matplotlib` (for generating plots)

# 

# Install with:

# 

# ```bash

# pip install psutil matplotlib

# ```

# 

# ---

# 

# \## 📬 Feedback \& Contributions

# 

# Feel free to open issues or submit pull requests for suggestions, bugs, or improvements.

# 

# ---

