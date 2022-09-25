from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter


# Disable automatic YAML aliases
class NonAliasingRTRepresenter(RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True


yaml = YAML()
yaml.Representer = NonAliasingRTRepresenter
