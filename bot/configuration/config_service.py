import yaml


class ConfigService:
    def __init__(self, config_name):
        self.config_name = config_name

    def load_yaml(self):
        with open(f"config/{self.config_name}.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def dump_to_yaml(self, data):
        with open(f"config/{self.config_name}.yaml", "w", encoding="utf-8") as file:
            yaml.dump(
                data,
                file,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            )

    def set_section_value(self, section_name, value):
        data = self.load_yaml()
        data[section_name] = value
        self.dump_to_yaml(data)

    def get_section_value(self, section_name):
        return self.load_yaml()[section_name]


if __name__ == "__main__":
    pass
