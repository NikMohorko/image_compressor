import pytest
from image import Img
from PIL import UnidentifiedImageError


@pytest.fixture
def img():
    return Img('tests/test_images/1.jpg', 0.98, 'temp/')


def test_check_extension(img):
    img.check_extension()


def test_load_and_save(img):
    img.load()
    img.save('', 80, 0)


def test_get_optimal_quality(img):
    img.load()
    assert 0 < img.get_optimal_quality() < 100


def test_invalid_extension():
    img = Img('tests/test_images/3.bmp', 0.98, 'temp/')
    with pytest.raises(TypeError):
        img.check_extension()


def test_load_unidentified_image():
    img = Img('tests/test_images/4.jpg', 0.98, 'temp/')
    with pytest.raises(UnidentifiedImageError):
        img.load()
