from PIL import Image
import os
from ssim import SSIMCalculator


class Img:

    def __init__(self, file_path: str, target_ssim: float, tempdir: str):
        self.file_path = file_path
        self.target_ssim = target_ssim
        self.tempdir = tempdir
        self.image_obj = None
        self.optimal_quality = None
        self.width = None
        self.height = None

        if not os.path.exists(tempdir):
            os.mkdir(tempdir)

    def load(self):
        self.image_obj = Image.open(self.file_path, 'r')
        self.width, self.height = self.image_obj.size

    def check_extension(self):
        if not self.file_path.endswith(('.jpg', '.jpeg')):
            raise TypeError

    def save(self, output_dir, quality, subsampling):
        self.image_obj.save(os.path.join(output_dir, os.path.basename(self.file_path)), 'JPEG', quality=round(quality),
                            subsampling=subsampling)

    def resize(self, maximum_dimension):

        if maximum_dimension is not None:
            if self.width > self.height:
                # Change to the set maximum, or keep it the same if already lower
                new_width = min(self.width, maximum_dimension)
                new_height = round(self.height * new_width / self.width)

            else:
                new_height = min(self.height, maximum_dimension)
                new_width = round(self.width * new_height / self.width)

            if new_height != self.height and new_width != self.width:
                self.image_obj = self.image_obj.resize((new_width, new_height))
                self.width, self.height = self.image_obj.size

    def get_optimal_quality(self):
        """Iterative loop to determine optimal quality for set SSIM value."""

        # Starting quality
        current_quality = 5

        # Quality increment for each iteration
        quality_increment = 3

        # Starting error
        current_error = 1

        # Whether SSIM value is above or below target
        under_target = True

        # Accepted SSIM deviation at the end of iteration
        allowed_ssim_error = 0.001

        # Initial temp image for SSIM calculation
        self.save(self.tempdir, current_quality, 0)

        while current_error > allowed_ssim_error:

            calculator = SSIMCalculator(self.file_path,
                                        os.path.join(self.tempdir, os.path.basename(self.file_path)), 20)

            current_error = self.target_ssim - calculator.calculate_ssim()

            # Change direction and reduce increment when target value is crossed
            if (current_error > 0) != under_target:
                under_target = not under_target
                quality_increment = - quality_increment / 2
                current_quality += quality_increment

            else:
                current_quality += quality_increment

            # Save temp image for SSIM calculation
            self.save(self.tempdir, current_quality, 0)

        return current_quality
