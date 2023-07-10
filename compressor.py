import typer
from typing_extensions import Annotated
import os
from PIL import UnidentifiedImageError
from shutil import rmtree
import logging

from image import Img


def compressor(input_dir: Annotated[str, typer.Argument(help='Directory with original images')],
               output_dir: Annotated[str, typer.Argument(help='Output directory for compressed images')],
               max_dimension: Annotated[int, typer.Argument(help='Maximum dimension [px]')] = None,
               ssim_factor: Annotated[float, typer.Argument(help='SSIM factor [0-1.0]')] = 0.97):

    # Input parameter validation
    if ssim_factor <= 0 or ssim_factor >= 1:
        raise ValueError('SSIM factor should be between 0 and 1.')

    if (not isinstance(max_dimension, int) and max_dimension is not None or
            isinstance(max_dimension, int) and max_dimension <= 0):
        raise ValueError('Maximum dimension should be a positive number.')

    temp_dir = 'temp'
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='log.txt', encoding='utf-8',
                        level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S')

    failed, complete = 0, 0
    original_file_size_sum = 0
    compressed_file_size_sum = 0

    with typer.progressbar(os.listdir(input_dir), label='Processing') as filenames:
        for filename in filenames:

            image = Img(os.path.join(input_dir, filename), ssim_factor, temp_dir)

            try:
                image.check_extension()
            except TypeError:
                failed += 1
                logging.error(f'Image {filename} skipped - unsupported extension.')
                continue

            try:
                image.load()
            except UnidentifiedImageError:
                failed += 1
                logging.error(f'Image {filename} skipped - file could not be read.')
                continue

            try:
                optimal_quality = image.get_optimal_quality()
            except AttributeError as exc:
                logging.error(f'Image {filename} skipped - {exc}.')
                failed += 1
                continue

            image.resize(max_dimension)

            try:
                image.save(output_dir, optimal_quality, 0)
            except OSError:
                failed += 1
                logging.error(f'Image {filename} skipped - file could not be saved.')
            else:
                complete += 1
                original_size = round(os.path.getsize(os.path.join(input_dir, filename)) / 1024)
                compressed_size = round(os.path.getsize(os.path.join(output_dir, filename)) / 1024)
                original_file_size_sum += original_size
                compressed_file_size_sum += compressed_size

                logging.info(f'Image {filename} successfully processed. Quality used: {round(optimal_quality)}, '
                             f'Original file size: {original_size} kB, Compressed file size: {compressed_size} kB.')

    size_saved_percentage = round((1 - compressed_file_size_sum / original_file_size_sum) * 100)

    logging.info(f'Processing completed. Successful: {complete}, failed: {failed}, '
                 f'average image size savings: {size_saved_percentage} %.')

    print(f'Processing completed. Successful: {complete}, failed: {failed}, '
          f'average image size savings: {size_saved_percentage} %.')

    rmtree(temp_dir)


if __name__ == "__main__":
    typer.run(compressor)
