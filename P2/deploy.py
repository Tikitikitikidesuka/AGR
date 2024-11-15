import os
import subprocess
import logging
from pathlib import Path
from config import load_configuration, Configuration, Machine
from network_generator.generator import NetworkGenerator
from vm_xml_builder import VmXmlBuilder

CONFIG_FILE = "config.toml"
INTERFACE_FILE_SUFFIX = "-interfaces"
LINK_FILE_SUFFIX = ".link"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
        logging.FileHandler('vm_creation.log')  # Log to a file
    ]
)


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
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {directory}")
        except Exception as e:
            logging.error(f"Error creating directory {directory}: {e}")


def create_xml_file(machine: Machine, config: Configuration) -> None:
    try:
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
        logging.info(f"XML file for machine {machine.name} created.")
    except Exception as e:
        logging.error(f"Error creating XML file for machine {machine.name}: {e}")


def create_image_file(machine: Machine, config: Configuration) -> None:
    try:
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
        logging.info(f"Image file for machine {machine.name} created at {output_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating image file for machine {machine.name}: {e}")


def copy_file_to_vm(image_path: str, src_path: str, dest_path: str) -> None:
    try:
        cmd = ["sudo", "virt-copy-in", "-a", image_path, src_path, dest_path]
        subprocess.run(cmd, check=True)
        logging.info(f"Copied file {src_path} to {dest_path} in VM image.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error copying file {src_path} to {dest_path} in VM image: {e}")


def create_vm(machine: Machine, config: Configuration) -> None:
    try:
        create_xml_file(machine, config)
        create_image_file(machine, config)

        xml_path = Path(config.general.xml_output_dir) / machine_xml_filename(machine.name)
        image_path = Path(config.general.disk_output_dir) / machine_img_filename(machine.name)

        # Register VM to libvirt
        subprocess.run(["sudo", "virsh", "define", str(xml_path)], check=True)
        logging.info(f"VM {machine.name} registered with libvirt.")

        # Generate and copy network config files
        network_files_dir = Path(config.general.network_config_output_dir)
        machine_network_config_dir = network_files_dir / machine_sanitized_name(machine.name)
        machine_network_config_dir.mkdir(parents=True, exist_ok=True)
        NetworkGenerator.write_network_config_files(
            machine, str(machine_network_config_dir), INTERFACE_FILE_SUFFIX, LINK_FILE_SUFFIX
        )
        logging.info(f"Network config files for machine {machine.name} generated.")

        for file in os.listdir(machine_network_config_dir):
            file_path = os.path.join(machine_network_config_dir, file)
            if os.path.isfile(file_path):
                dest_path = (
                    "/etc/systemd/network/"
                    if file.endswith(LINK_FILE_SUFFIX)
                    else "/etc/network/interfaces"
                )
                copy_file_to_vm(str(image_path), file_path, dest_path)

    except Exception as e:
        logging.error(f"Error creating VM {machine.name}: {e}")


def main():
    try:
        config = load_configuration(CONFIG_FILE)
        logging.info("Configuration loaded successfully.")

        create_output_directories(config)

        for machine in config.servers + config.routers:
            create_vm(machine, config)

        logging.info("All VMs and network configurations created successfully.")

    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == '__main__':
    main()
