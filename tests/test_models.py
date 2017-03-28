import pytest

import src.models as models


def test_crumb_model():
    assert models.Crumb.__tablename__ == 'crumbs'
