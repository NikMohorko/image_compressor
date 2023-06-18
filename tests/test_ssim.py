from ssim import SSIMCalculator
import pytest


def test_image_too_small():
    with pytest.raises(AttributeError):
        SSIMCalculator('tests/test_images/small.jpg', 'tests/test_images/small.jpg', 20)


def test_returned_ssim_value():
    calculator = SSIMCalculator('tests/test_images/1.jpg', 'tests/test_images/2.jpg', 20)
    assert 0.9 < calculator.calculate_ssim() < 1
