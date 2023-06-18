from compressor import compressor
import pytest


def test_pass_wrong_ssim_value():
    with pytest.raises(ValueError):
        assert compressor('', '', 2)
