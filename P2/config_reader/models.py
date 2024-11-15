from dataclasses import dataclass
from typing import List


@dataclass
class Interface:
    bridge: str
    ip: str
    mask: str


@dataclass
class RouteRule:
    destination: str
    via: str


@dataclass
class Machine:
    name: str
    interfaces: List[Interface]


@dataclass
class Server(Machine):
    gateway: str


@dataclass
class Router(Machine):
    route_rules: List[RouteRule]


@dataclass
class General:
    xml_template_path: str
    base_disk_path: str
    xml_output_dir: str
    disk_output_dir: str


@dataclass
class Configuration:
    general: General
    servers: List[Server]
    routers: List[Router]
