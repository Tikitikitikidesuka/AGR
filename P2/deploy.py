import os
from pathlib import Path
from config_reader import load_configuration, Configuration, Machine
from vm_xml_builder import VmXmlBuilder

CONFIG_FILE = "config.toml"


def machine_img_filename(name: str):
    IMAGE_SUFFIX = "-img.qcow2"
    sanitized_name = name.lower().replace(' ', '')
    return f"{sanitized_name}{IMAGE_SUFFIX}"


def machine_xml_filename(name: str):
    IMAGE_SUFFIX = "-vm.xml"
    sanitized_name = name.lower().replace(' ', '')
    return f"{sanitized_name}{IMAGE_SUFFIX}"


def create_xml_file(machine: Machine, config: Configuration):
    VmXmlBuilder.from_template(config.general.xml_template_path) \
        .name(machine.name) \
        .bridges([interface.bridge for interface in machine.interfaces]) \
        .image_path(str(Path(config.general.base_disk_path).parent / machine_img_filename(machine.name))) \
        .output_path(str(Path(config.general.xml_output_dir) / machine_xml_filename(machine.name))) \
        .build()


def create_image_file(machine: Machine, config: Configuration):
    os.system(
        f"qemu-img create -f qcow2 -b {config.general.base_disk_path} -F qcow2 {machine_img_filename(machine.name)}")


def create_vm(machine: Machine, config: Configuration):
    create_xml_file(machine, config)
    create_image_file(machine, config)

    # Register vm to virsh
    os.system(f"sudo virsh define {machine_xml_filename(machine.name)}")

    # Copy interfaces config
    pass


def main():
    config = load_configuration(CONFIG_FILE)
    for machine in config.servers + config.routers:
        create_vm(machine, config)


if __name__ == '__main__':
    main()
