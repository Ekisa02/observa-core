import os
import torch
from app.core.model import ModelWrapper, ensure_model_exists


def test_model_save_load(tmp_path):
    # create small model and save
    model_file = tmp_path / "m.pt"
    mw = ModelWrapper(input_dim=4, latent_dim=2)
    mw.save(str(model_file))

    assert os.path.exists(str(model_file))

    mw2 = ModelWrapper(input_dim=4, latent_dim=2)
    mw2.load(str(model_file))

    # score with a simple vector
    score = mw2.score([0.1, 0.2, 0.3, 0.4])
    assert isinstance(score, float)


def test_ensure_model_exists(tmp_path):
    f = tmp_path / "mustexist.pt"
    path = str(f)
    # ensure_model_exists creates file
    ensure_model_exists(path, input_dim=6)
    assert os.path.exists(path)
