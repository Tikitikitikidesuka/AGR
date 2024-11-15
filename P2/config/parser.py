import tomllib
from .models import Interface, RouteRule, Server, Router, General, Configuration


def parse_interfaces(interfaces_data):
    return [Interface(**iface) for iface in interfaces_data]


def parse_route_rules(route_rules_data):
    return [RouteRule(**rule) for rule in route_rules_data]


def parse_servers(servers_data):
    servers = []
    for server_data in servers_data:
        interfaces = parse_interfaces(server_data.get("Interface", []))
        servers.append(Server(
            name=server_data["name"],
            gateway=server_data["gateway"],
            interfaces=interfaces
        ))
    return servers


def parse_routers(routers_data):
    routers = []
    for router_data in routers_data:
        interfaces = parse_interfaces(router_data.get("Interface", []))
        route_rules = parse_route_rules(router_data.get("RouteRule", []))
        routers.append(Router(
            name=router_data["name"],
            interfaces=interfaces,
            route_rules=route_rules
        ))
    return routers


def parse_general(general_data):
    return General(**general_data)


def load_configuration(file_path: str) -> Configuration:
    with open(file_path, "rb") as f:
        data = tomllib.load(f)

    general = parse_general(data.get("General", {}))
    servers = parse_servers(data.get("Server", []))
    routers = parse_routers(data.get("Router", []))
    return Configuration(general=general, servers=servers, routers=routers)
