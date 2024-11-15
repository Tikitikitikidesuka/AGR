import subprocess
import logging
from pathlib import Path
from deploy import CONFIG_FILE
from config import load_configuration, Configuration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
        logging.FileHandler('cleanup.log')  # Log to a file
    ]
)


def delete_bridges(config: Configuration) -> None:
    for machine in config.servers + config.routers:
        for interface in machine.interfaces:
            bridge = interface.bridge
            try:
                # Check if the bridge exists and remove it using ip link
                subprocess.run(['ip', 'link', 'set', bridge, 'down'], check=True)
                subprocess.run(['ip', 'link', 'delete', bridge], check=True)
                logging.info(f"Bridge {bridge} deleted.")
            except subprocess.CalledProcessError:
                logging.warning(f"Bridge {bridge} not found or could not be deleted.")


def delete_vms(config: Configuration) -> None:
    for machine in config.servers + config.routers:
        vm_name = machine.name
        try:
            # Stop and undefine the VM (if it's running)
            subprocess.run(['virsh', 'destroy', vm_name], check=True)
            subprocess.run(['virsh', 'undefine', vm_name], check=True)
            logging.info(f"VM {vm_name} destroyed and undefined.")
        except subprocess.CalledProcessError:
            logging.warning(f"VM {vm_name} not found or could not be destroyed.")


def cleanup_directories(config: Configuration) -> None:
    try:
        # Remove network configuration, disk output, and XML output directories
        Path(config.general.network_config_output_dir).rmdir()
        logging.info(f"Removed network config directory: {config.general.network_config_output_dir}")
        Path(config.general.disk_output_dir).rmdir()
        logging.info(f"Removed disk output directory: {config.general.disk_output_dir}")
        Path(config.general.xml_output_dir).rmdir()
        logging.info(f"Removed XML output directory: {config.general.xml_output_dir}")
    except Exception as e:
        logging.error(f"Error while removing directories: {e}")


def main():
    # Load the configuration
    config = load_configuration(CONFIG_FILE)

    # Delete all bridges, VMs, and clean up directories
    delete_bridges(config)
    delete_vms(config)
    cleanup_directories(config)


if __name__ == '__main__':
    main()
