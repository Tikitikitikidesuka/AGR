import shutil
import subprocess
import logging
from pathlib import Path
from deploy import CONFIG_FILE
from config import load_configuration, Configuration


def delete_bridges(config: Configuration) -> None:
    for machine in config.servers + config.routers:
        for interface in machine.interfaces:
            bridge = interface.bridge

            try:
                subprocess.run(['ip', 'link', 'set', bridge, 'down'], check=True)
                logging.info(f"Bridge {bridge} stopped.")
            except FileNotFoundError as e:
                logging.error(f"Command not found: {e}")
            except subprocess.CalledProcessError as e:
                logging.warning(f"Bridge {bridge} not found or could not be stopped. Error: {e}")
            except Exception as e:
                logging.error(f"Unexpected error while processing bridge {bridge}: {e}")

            try:
                subprocess.run(['ip', 'link', 'delete', bridge], check=True)
                logging.info(f"Bridge {bridge} deleted.")
            except FileNotFoundError as e:
                logging.error(f"Command not found: {e}")
            except subprocess.CalledProcessError as e:
                logging.warning(f"Bridge {bridge} not found or could not be deleted. Error: {e}")
            except Exception as e:
                logging.error(f"Unexpected error while processing bridge {bridge}: {e}")


def delete_vms(config: Configuration) -> None:
    for machine in config.servers + config.routers:
        vm_name = machine.name

        try:
            subprocess.run(['virsh', 'destroy', vm_name], check=True)
            logging.info(f"VM {vm_name} destroyed.")
        except FileNotFoundError as e:
            logging.error(f"Command not found: {e}")
        except subprocess.CalledProcessError as e:
            logging.warning(f"VM {vm_name} could not be destroyed. Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while processing VM {vm_name}: {e}")

        try:
            subprocess.run(['virsh', 'undefine', vm_name], check=True)
            logging.info(f"VM {vm_name} undefined.")
        except FileNotFoundError as e:
            logging.error(f"Command not found: {e}")
        except subprocess.CalledProcessError as e:
            logging.warning(f"VM {vm_name} could not be undefined. Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while processing VM {vm_name}: {e}")


def cleanup_directories(config: Configuration) -> None:
    # Define a helper function to remove a directory even if it is not empty
    def remove_dir(dir_path: Path) -> None:
        try:
            shutil.rmtree(dir_path)  # Removes the directory and all of its contents
            logging.info(f"Removed directory: {dir_path}")
        except FileNotFoundError as e:
            logging.warning(f"Directory not found: {e}")
        except OSError as e:
            logging.error(f"Error removing directory: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while removing directory {dir_path}: {e}")

    # Attempt to remove each directory
    remove_dir(Path(config.general.network_config_output_dir))
    remove_dir(Path(config.general.disk_output_dir))
    remove_dir(Path(config.general.xml_output_dir))


def main():
    try:
        config = load_configuration(CONFIG_FILE)
    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error while loading configuration: {e}")
        return

    try:
        Path(config.general.cleaup_log_path).parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Output logs to the console
                logging.FileHandler(config.general.cleaup_log_path)  # Log to a file
            ]
        )
    except Exception as e:
        logging.error(f"Unexpected error while setting up logging: {e}")
        return

    # Execute cleanup functions
    try:
        delete_bridges(config)
    except Exception as e:
        logging.error(f"Error while deleting bridges: {e}")

    try:
        delete_vms(config)
    except Exception as e:
        logging.error(f"Error while deleting VMs: {e}")

    try:
        cleanup_directories(config)
    except Exception as e:
        logging.error(f"Error during directory cleanup: {e}")


if __name__ == '__main__':
    main()