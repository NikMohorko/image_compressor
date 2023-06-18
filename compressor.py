import typer
from typing_extensions import Annotated
import os
from PIL import UnidentifiedImageError
from shutil import rmtree

from image import Img


def compressor(input_dir: Annotated[str, typer.Argument(help='Directory with original images')],
               output_dir: Annotated[str, typer.Argument(help='Output directory for compressed images')],
               ssim_factor: Annotated[float, typer.Argument(help='SSIM factor [0-1.0]')] = 0.97):

    if ssim_factor <= 0 or ssim_factor >= 1:
        raise ValueError('SSIM factor should be between 0 and 1.')

    temp_dir = 'temp'
    failed, complete = 0, 0

    with typer.progressbar(os.listdir(input_dir), label='Processing') as filenames:
        for filename in filenames:

            image = Img(os.path.join(input_dir, filename), ssim_factor, temp_dir)

            try:
                image.check_extension()
            except TypeError:
                failed += 1
                continue

            try:
                image.load()
            except UnidentifiedImageError:
                failed += 1
                continue

            try:
                optimal_quality = image.get_optimal_quality()
            except AttributeError:
                failed += 1
                continue

            try:
                image.save(output_dir, optimal_quality, 0)
            except OSError:
                failed += 1
            else:
                complete += 1

    print(f'Processing completed. Successful: {complete}, failed: {failed}.')

    rmtree(temp_dir)


if __name__ == "__main__":
    typer.run(compressor)
