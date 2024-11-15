from config_reader import load_configuration
from vm_xml_builder import VmXmlBuilder

if __name__ == '__main__':
    # Load the configuration from the TOML file
    config = load_configuration("config.toml")

    # Access the general configuration
    print("General Configuration:")
    print(config.general)

    # Access the parsed configuration for servers and routers
    print("\nServers:")
    for server in config.servers:
        print(server)

    print("\nRouters:")
    for router in config.routers:
        print(router)

    VmXmlBuilder.from_template('base-vm.xml') \
        .name('test') \
        .bridges(['a', 'b']) \
        .image_path('img.qcow2') \
        .output_path('out.xd') \
        .build()