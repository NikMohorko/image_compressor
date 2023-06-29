from compressor import compressor
import pytest


def test_pass_wrong_ssim_value():
    with pytest.raises(ValueError, match='SSIM factor should be between 0 and 1.'):
        assert compressor('', '', None, 2)


def test_pass_wrong_max_dimension():
    with pytest.raises(ValueError, match='Maximum dimension should be a positive number.'):
        assert compressor('', '', -200, 0.97)
