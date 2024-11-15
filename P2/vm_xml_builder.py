from typing import List, Self

class VmXmlBuilder:
    def __init__(self, template_path: str) -> None:
        self._template_path = template_path
        self._name = None
        self._image_path = None
        self._bridges = []
        self._output_path = None

    def name(self, name: str) -> Self:
        self._name = name
        return self

    def image_path(self, image_path: str) -> Self:
        self._image_path = image_path
        return self

    def bridges(self, bridges: List[str]) -> Self:
        self._bridges = bridges
        return self

    def output_path(self, output_path: str) -> Self:
        self._output_path = output_path
        return self

    def build(self) -> None:
        # Validate required fields
        if not all([self._name, self._image_path, self._output_path]):
            raise ValueError("Name, image path, and output path must be set before building.")

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self._template_path, parser)
        
        # Set name and image path
        name_element = tree.xpath('/domain/name')[0]
        name_element.text = self._name

        image_path_element = tree.xpath('/domain/devices/disk/source')[0]
        image_path_element.set('file', self._image_path)
        
        # Remove existing bridge interfaces
        interfaces = tree.xpath('/domain/devices/interface[@type="bridge"]')
        devices = tree.xpath('/domain/devices')[0]
        for interface in interfaces:
            devices.remove(interface)
        
        # Add new bridge interfaces
        for bridge in self._bridges:
            interface = etree.SubElement(devices, 'interface', type='bridge')
            etree.SubElement(interface, 'source', bridge=bridge)
            etree.SubElement(interface, 'model', type='virtio')
        
        # Save the modified XML
        tree.write(self._output_path, pretty_print=True, encoding='utf-8', xml_declaration=True)

    @classmethod
    def from_template(cls, template_path: str) -> 'VmXmlBuilder':
        return cls(template_path)

if __name__ == "__main__":
    VmXmlBuilder.from_template('base-vm.xml') \
        .name('test') \
        .image_path('base-image.qcow2') \
        .output_path('test-vm.xml') \
        .bridges(['test-br-a', 'test-br-b']) \
        .build()