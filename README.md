# Watermarker

Python3.7 Library for watermarking images

## Installation

## Usage

- Check `example.py` or copy and paste the following code into your favorite text editor

```python
# Created by: Dare McAdewole <dare.dev.adewole@gmail.com>
from watermarker import Watermarker
from pathlib import Path

if __name__ == '__main__':
    if (Watermarker.watermark(
        '.../gordon.png',
        '.../echwoodd/lo.png',
        '.../echwood-steve.png',
        Watermarker.Position.top_right
    )):
        print('Image watermarked successfully!')
    else:
        print('Image could not be watermarked'
```

## Contributors

- Dare McAdewole
