from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter


class NonAliasingRTRepresenter(RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True


yaml = YAML()
yaml.Representer = NonAliasingRTRepresenter
