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
