
import pytest

from src.sed.models import build_sednet, build_sedgru

DEFAULTS = dict(input_shape=(10, 32))
# examples of valid models
VALID_MODELS = {
    'sednet_default': (build_sednet, dict(**DEFAULTS)),
    'sedgru_default': (build_sedgru, dict(**DEFAULTS)),
}

@pytest.mark.parametrize('name', VALID_MODELS.keys())
def test_sed_model_build(name):

    build_func, params = VALID_MODELS[name]

    # should not give exception
    model = build_func(**params)

    assert model
    assert model.fit

