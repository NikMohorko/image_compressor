# Image compressor

Command-line application for lossy compression of JPEG images, ideal for improving
load time of websites.

Each image's final quality is iteratively determined using the structural similarity (SSIM) algorithm, so 
that the visual difference between original and compressed picture is optimal. Detailed results 
are saved to `log.txt`.

The SSIM algorithm is implemented in Cython to increase performance.

Supported image types are: JPEG

# Setup

1. Use pip to install requirements:

```bash
pip install -r requirements.txt
```

2. Compile the Cython module:
```bash
python setup.py build_ext --inplace
```
3. Run:
```bash
python compressor.py [input dir] [output dir] [maximum dimension] [SSIM factor]
```

### Arguments
- `input dir`: Path to directory with original images
- `output dir`: Path to directory where compressed images will be stored
- `maximum dimension`: Optional; Maximum dimension in pixels to further reduce file size. If used, the aspect ratio
will be preserved and width/height (whichever larger) will be set to this number.
- `SSIM factor`: Optional; [0-1.0] SSIM factor, default value of 0.97 usually gives optimal results for most images

## Technologies used
- Python 3.9
- Cython

## Resources

[Wang, Zhou; Bovik, A.C.; Sheikh, H.R.; Simoncelli, E.P. (2004-04-01). "Image quality assessment: from error visibility to structural similarity". IEEE Transactions on Image Processing. 13 (4): 600–612. ](https://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf)

[Structural similarity](https://en.wikipedia.org/wiki/Structural_similarity)