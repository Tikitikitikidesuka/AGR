import os
from pathlib import Path
import subprocess
from config import load_configuration, Configuration, Machine
from network_generator.generator import NetworkGenerator
from vm_xml_builder import VmXmlBuilder

CONFIG_FILE = "config.toml"
INTERFACE_FILE_SUFFIX = "-interfaces"
LINK_FILE_SUFFIX = ".link"


def machine_sanitized_name(name: str) -> str:
    return name.lower().replace(' ', '')


def machine_img_filename(name: str) -> str:
    IMAGE_SUFFIX = "-img.qcow2"
    return f"{machine_sanitized_name(name)}{IMAGE_SUFFIX}"


def machine_xml_filename(name: str) -> str:
    XML_SUFFIX = "-vm.xml"
    return f"{machine_sanitized_name(name)}{XML_SUFFIX}"


def create_output_directories(config: Configuration) -> None:
    for directory in [
        config.general.xml_output_dir,
        config.general.disk_output_dir,
        config.general.network_config_output_dir,
    ]:
        Path(directory).mkdir(parents=True, exist_ok=True)


def create_xml_file(machine: Machine, config: Configuration) -> None:
    xml_builder = VmXmlBuilder.from_template(config.general.xml_template_path)
    xml_builder.name(machine.name)
    xml_builder.bridges([interface.bridge for interface in machine.interfaces])
    xml_builder.image_path(
        str(Path(config.general.base_disk_path).parent / machine_img_filename(machine.name))
    )
    xml_builder.output_path(
        str(Path(config.general.xml_output_dir) / machine_xml_filename(machine.name))
    )
    xml_builder.build()


def create_image_file(machine: Machine, config: Configuration):
    output_path = Path(config.general.disk_output_dir) / machine_img_filename(machine.name)
    base_disk_path = config.general.base_disk_path
    cmd = [
        "qemu-img",
        "create",
        "-f",
        "qcow2",
        "-b",
        Path(base_disk_path).absolute(),
        "-F",
        "qcow2",
        output_path.absolute(),
    ]
    subprocess.run(cmd, check=True)


def copy_file_to_vm(image_path: str, src_path: str, dest_path: str):
    cmd = ["sudo", "virt-copy-in", "-a", image_path, src_path, dest_path]
    subprocess.run(cmd, check=True)


def create_vm(machine: Machine, config: Configuration):
    create_xml_file(machine, config)
    create_image_file(machine, config)

    xml_path = Path(config.general.xml_output_dir) / machine_xml_filename(machine.name)
    image_path = Path(config.general.disk_output_dir) / machine_img_filename(machine.name)

    # Register VM to libvirt
    subprocess.run(["sudo", "virsh", "define", str(xml_path)], check=True)

    # Generate and copy network config files
    network_files_dir = Path(config.general.network_config_output_dir)
    machine_network_config_dir = network_files_dir / machine_sanitized_name(machine.name)
    machine_network_config_dir.mkdir(parents=True, exist_ok=True)
    NetworkGenerator.write_network_config_files(
        machine, str(machine_network_config_dir), INTERFACE_FILE_SUFFIX, LINK_FILE_SUFFIX
    )

    for file in os.listdir(machine_network_config_dir):
        file_path = os.path.join(machine_network_config_dir, file)
        if os.path.isfile(file_path):
            dest_path = (
                "/etc/systemd/network/"
                if file.endswith(LINK_FILE_SUFFIX)
                else "/etc/network/interfaces"
            )
            copy_file_to_vm(str(image_path), file_path, dest_path)


def main():
    config = load_configuration(CONFIG_FILE)
    create_output_directories(config)

    for machine in config.servers + config.routers:
        create_vm(machine, config)


if __name__ == '__main__':
    main()
