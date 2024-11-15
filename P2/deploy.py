from pathlib import Path
from config_reader import load_configuration, Configuration
from vm_xml_builder import VmXmlBuilder

def create_xml_files(config: Configuration):
    for item in config.servers + config.routers:
        XML_SUFFIX = "-vm.xml"
        IMAGE_SUFFIX = "-img.qcow"

        sanitized_name = item.name.lower().replace(' ', '')

        VmXmlBuilder.from_template(config.general.xml_template_path) \
            .name(item.name) \
            .bridges([interface.bridge for interface in item.interfaces]) \
            .image_path(str(Path(config.general.base_disk_path).parent / f"{sanitized_name}{IMAGE_SUFFIX}")) \
            .output_path(str(Path(config.general.xml_output_dir) / f"{sanitized_name}{XML_SUFFIX}")) \
            .build()

if __name__ == '__main__':
    config = load_configuration("config.toml")
    create_xml_files(config)