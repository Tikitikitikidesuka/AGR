import os
from pathlib import Path
from config import load_configuration, Configuration, Machine
from network_generator.generator import NetworkGenerator
from vm_xml_builder import VmXmlBuilder

CONFIG_FILE = "config.toml"
INTERFACE_FILE_SUFFIX = "-interfaces"
LINK_FILE_SUFFIX = ".link"


def machine_sanitez_name(name: str) -> str:
    return name.lower().replace(' ', '')


def machine_img_filename(name: str) -> str:
    IMAGE_SUFFIX = "-img.qcow2"
    return f"{machine_sanitez_name(name)}{IMAGE_SUFFIX}"


def machine_xml_filename(name: str) -> str:
    XML_SUFFIX = "-vm.xml"
    return f"{machine_sanitez_name(name)}{XML_SUFFIX}"


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

    xml_path = Path(config.general.xml_output_dir) / machine_xml_filename(machine.name)
    image_path = Path(config.general.disk_output_dir) / machine_img_filename(machine.name)
    network_files_dir = Path(config.general.network_config_output_dir)

    # Register vm to virsh
    os.system(f"sudo virsh define {xml_path}")

    # Pasos importantes que se me van a olvidar:
    # 1. Pasar el fichero interface de cada máquina a /etc/network/interfaces
    # 2. Pasar los ficheros link de cada máquina a /etc/systemd/network/{nombrefichero}.link

    # Copy network config files to the machine
    for file in os.listdir(network_files_dir / machine.name):
        file_path = os.path.join(network_files_dir / machine.name, file)
        if os.path.isfile(file_path) and file.endswith(LINK_FILE_SUFFIX):
            os.system(f"sudo virt-copy-in -a {image_path} {file_path} /etc/systemd/network/")
        elif os.path.isfile(file_path) and file.endswith(INTERFACE_FILE_SUFFIX):
            os.system(f"sudo virt-copy-in -a {image_path} {file_path} /etc/network/interfaces")

    # Pasar las llamadas de os.system a subprocess !!!


def main():
    config = load_configuration(CONFIG_FILE)
    """output_dir = Path(config.general.network_config_output_dir) / machine_sanitez_name(config.routers[-1].name)
    output_dir.mkdir(parents=True, exist_ok=True)
    NetworkGenerator.write_network_config_files(config.routers[0], str(output_dir), INTERFACE_FILE_SUFFIX, LINK_FILE_SUFFIX)
    create_xml_file(config.routers[0], config)"""
    for machine in config.servers + config.routers:
        create_vm(machine, config)


if __name__ == '__main__':
    main()
