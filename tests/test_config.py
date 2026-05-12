from core.config.miniyaml import load_simple_yaml

def test_config_example_loads():
    d=load_simple_yaml('atlas.config.example.yaml')
    assert 'paths' in d
