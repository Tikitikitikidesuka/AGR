from typing import List
from pathlib import Path

from config import Interface, RouteRule, Machine, Server, Router


class NetworkGenerator:
    @staticmethod
    def _generate_interface_config(interface: Interface) -> str:
        return f"""auto {interface.id}
iface {interface.id} inet static
    address {interface.ip}
    netmask {interface.mask}
"""

    @staticmethod
    def _generate_route_rules(rules: List[RouteRule]) -> str:
        return "\n".join(f"    up ip route add {rule.destination} via {rule.via}"
                         for rule in rules)

    @classmethod
    def generate_machine_interface_file(cls, machine: Machine) -> str:
        config_parts = [
            "auto lo",
            "iface lo inet loopback\n"
        ]

        for interface in machine.interfaces:
            config_parts.append(cls._generate_interface_config(interface))

        if isinstance(machine, Server) and machine.gateway:
            config_parts.append(f"    gateway {machine.gateway}\n")

        if isinstance(machine, Router) and machine.route_rules:
            config_parts.append(cls._generate_route_rules(machine.route_rules))

        return "\n".join(config_parts)

    @classmethod
    def generate_machine_interface_link_file(cls, interface: Interface) -> str:
        return f"""[Match]
MACAddress={interface.mac}

[Link]
Name={interface.id}
"""

    @classmethod
    def write_network_config_files(cls, machine: Machine, output_dir: str, interface_file_suffix: str, link_file_suffix: str) -> None:
        with open(Path(output_dir) / (machine.name + interface_file_suffix), "w") as f:
            f.write(cls.generate_machine_interface_file(machine))
        for interface in machine.interfaces:
            with open(Path(output_dir) / (interface.id + link_file_suffix), "w") as f:
                f.write(cls.generate_machine_interface_link_file(interface))