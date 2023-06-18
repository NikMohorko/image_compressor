from PIL import Image
from math import ceil

cdef class SSIMCalculator:
    cdef dict __dict__
    cdef int tile_size
    cdef int tile_pixel_count
    cdef int width
    cdef int height
    cdef double c1
    cdef double c2
    cdef int number_of_bands

    def __init__(self, str image1_path, str image2_path, int tile_size):
        self.image1 = Image.open(image1_path)
        self.image2 = Image.open(image2_path)
        self.width, self.height = self.image1.size
        self.tile_size = tile_size
        self.tile_pixel_count = tile_size * tile_size

        if self.width < self.tile_size or self.height < self.tile_size:
            raise AttributeError(f'Image is smaller than tile size ({self.tile_size} px).')

        self.c1 = 0
        self.c2 = 0
        self.number_of_bands = 0

    cpdef double calculate_ssim(self):

        self.set_constants()

        # Calculate average SSIM by dividing sum of all SSIM values by number if tiles and bands
        return self.calculate_ssim_sum() / \
            (ceil(self.width / self.tile_size) * ceil(self.height / self.tile_size) * self.number_of_bands)

    cdef set_constants(self):
        cdef int din_range = 255  # 2 ** {number of bits per pixel} - 1
        self.c1 = (0.01 * din_range) * (0.01 * din_range)
        self.c2 = (0.03 * din_range) * (0.03 * din_range)
        self.number_of_bands = len(self.image1.getbands())

    cdef double calculate_ssim_sum(self):

        cdef double ssim_sum = 0
        cdef int pixel_sum_0
        cdef int pixel_sum_1
        cdef double pixel_avg_0
        cdef double pixel_avg_1
        cdef double covariance
        cdef double variance0
        cdef double variance1
        cdef int x
        cdef int y
        cdef int b
        cdef list tile0_pixel_values
        cdef list tile1_pixel_values
        cdef int p0
        cdef int p1
        cdef int pixel_value

        for x in range(0, self.width, self.tile_size):
            for y in range(0, self.height, self.tile_size):

                # Create tile for both images
                tile0 = self.image1.crop((x, y, x + self.tile_size, y + self.tile_size))
                tile1 = self.image2.crop((x, y, x + self.tile_size, y + self.tile_size))

                # For each color channel
                for b in range(self.number_of_bands):

                    tile0_pixel_values, tile1_pixel_values = list(tile0.getdata(band=b)), list(tile1.getdata(band=b))

                    pixel_sum_0 = sum(tile0_pixel_values)
                    pixel_sum_1 = sum(tile1_pixel_values)

                    pixel_avg_0 = pixel_sum_0 / self.tile_pixel_count
                    pixel_avg_1 = pixel_sum_1 / self.tile_pixel_count

                    covariance = sum([(p0 - pixel_avg_0) * (p1 - pixel_avg_1) for
                        p0, p1 in zip(tile0_pixel_values, tile1_pixel_values)]) / self.tile_pixel_count

                    variance0 = sum([(pixel_value - pixel_avg_0) * (pixel_value - pixel_avg_0) for
                        pixel_value in tile0_pixel_values]) / self.tile_pixel_count
                    variance1 = sum([(pixel_value - pixel_avg_1) * (pixel_value - pixel_avg_1) for
                        pixel_value in tile1_pixel_values]) / self.tile_pixel_count

                    ssim_sum += (2 * pixel_avg_0 * pixel_avg_1 + self.c1) * \
                                (2 * covariance + self.c2) / \
                                ((pixel_avg_0 * pixel_avg_0 + pixel_avg_1 * pixel_avg_1 + self.c1) *
                                 (variance0 + variance1 + self.c2))

        return ssim_sum
