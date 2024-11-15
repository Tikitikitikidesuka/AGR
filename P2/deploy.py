import os
from pathlib import Path
from config_reader import load_configuration, Configuration
from vm_xml_builder import VmXmlBuilder

def machine_img_filename(name: str):
    IMAGE_SUFFIX = "-img.qcow2"
    sanitized_name = name.lower().replace(' ', '')
    return f"{sanitized_name}{IMAGE_SUFFIX}"

def machine_xml_filename(name: str):
    IMAGE_SUFFIX = "-vm.xml"
    sanitized_name = name.lower().replace(' ', '')
    return f"{sanitized_name}{IMAGE_SUFFIX}"

def create_xml_files(config: Configuration):
    for item in config.servers + config.routers:
        VmXmlBuilder.from_template(config.general.xml_template_path) \
            .name(item.name) \
            .bridges([interface.bridge for interface in item.interfaces]) \
            .image_path(str(Path(config.general.base_disk_path).parent / machine_img_filename(item.name))) \
            .output_path(str(Path(config.general.xml_output_dir) / machine_xml_filename(item.name))) \
            .build()

def create_images(config: Configuration):
    for server in config.servers:
        # Create new image file
        os.system(f"qemu-img create -f qcow2 -b {config.general.base_disk_path} -F qxow2 {machine_img_filename(server.name)}")
        # Register vm to virsh
        os.system(f"sudo virsh define {machine_xml_filename(server.name)}")
        # Copy interfaces config


    for router in config.routers:
        pass


if __name__ == '__main__':
    config = load_configuration("config.toml")
    create_xml_files(config)
    create_images(config)