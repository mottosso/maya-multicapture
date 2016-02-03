# multicapture

Capture multiple cameras at once.

### Usage

Import this single module without dependencies, and run the following.

```python
import multicapture
multicapture.capture()
```

### Limitations

1. You must have four visible viewports prior to running this command.
2. Captured viewports are put into a GridLayout at their original sizes; try and keep them similar prior to capturing.
3. On Linux, overlapping windows are captured alongside viewport

### Goals

1. Support arbitrary amount of cameras
2. Provide GUI to arrange/re-arrange layout of up to 4 views, arranged as 2x2, 1x2 or 2x1, both vertically and horizontally.
3. Pre-conditions are fixed; handle imperfect conditions better.

```
2x2              1x2h           1x2v      
 ___________     ___________    ___________
|     |     |   |           |  |     |     |
|_____|_____|   |___________|  |     |_____|  
|     |     |   |     |     |  |     |     |
|_____|_____|   |_____|_____|  |_____|_____|
