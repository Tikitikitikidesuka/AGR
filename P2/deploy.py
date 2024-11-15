from lxml import etree
from vm_xml_builder import VmXmlBuilder

NETWORK_CONFIG = {
    'Server': {
        'bridge': 'br-server',
        'ip': ['10.0.0.1'],
        'gateway': ['10.0.0.2'],
        'mask': ['255.255.255.0'],
        'is_router': False,
    },
    'Router_D': {
        'bridge': ['br-server', 'br-cd'],
        'ip': ['10.0.0.2', '10.1.0.1'],
        'mask': ['255.255.255.252', '255.255.255.252'],
        'is_router': True,
        'routes': [
            {'dest': '10.0.0.0/24', 'via': '10.0.0.2'},
            {'dest': '0.0.0.0/0', 'via': '10.1.0.1'},
        ]
    }
}

if __name__ == '__main__':
    for NAME in NETWORK_CONFIG:
        print(NAME)
