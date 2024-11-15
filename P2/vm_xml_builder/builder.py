from lxml import etree
from typing import List, Optional, Self


class VmXmlBuilder:
    def __init__(self, template_path: str) -> None:
        if not template_path or not isinstance(template_path, str):
            raise ValueError("Template path must be a non-empty string.")
        self._template_path = template_path
        self._name: Optional[str] = None
        self._image_path: Optional[str] = None
        self._bridges: List[str] = []
        self._output_path: Optional[str] = None

    def name(self, name: str) -> Self:
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = name
        return self

    def image_path(self, image_path: str) -> Self:
        if not image_path or not isinstance(image_path, str):
            raise ValueError("Image path must be a non-empty string.")
        self._image_path = image_path
        return self

    def bridges(self, bridges: List[str]) -> Self:
        if not isinstance(bridges, list) or not all(isinstance(bridge, str) and bridge for bridge in bridges):
            raise ValueError("Bridges must be a list of non-empty strings.")
        self._bridges = bridges
        return self

    def output_path(self, output_path: str) -> Self:
        if not output_path or not isinstance(output_path, str):
            raise ValueError("Output path must be a non-empty string.")
        self._output_path = output_path
        return self

    def build(self) -> None:
        # Validate required fields
        if not all([self._name, self._image_path, self._output_path]):
            raise ValueError("Name, image path, and output path must be set before building.")

        # Parse the XML template
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(self._template_path, parser)
        except (etree.XMLSyntaxError, OSError) as e:
            raise ValueError(f"Error parsing XML template: {e}")

        # Update the name
        name_elements = tree.xpath('/domain/name')
        if not name_elements:
            raise ValueError("Template does not contain a '/domain/name' element.")
        name_elements[0].text = self._name

        # Update the image path
        image_path_elements = tree.xpath('/domain/devices/disk/source')
        if not image_path_elements:
            raise ValueError("Template does not contain a '/domain/devices/disk/source' element.")
        image_path_elements[0].set('file', self._image_path)

        # Remove existing bridge interfaces
        devices_elements = tree.xpath('/domain/devices')
        if not devices_elements:
            raise ValueError("Template does not contain a '/domain/devices' element.")
        devices = devices_elements[0]
        for interface in tree.xpath('/domain/devices/interface[@type="bridge"]'):
            devices.remove(interface)

        # Add new bridge interfaces
        for bridge in self._bridges:
            interface = etree.SubElement(devices, 'interface', type='bridge')
            etree.SubElement(interface, 'source', bridge=bridge)
            etree.SubElement(interface, 'model', type='virtio')

        # Save the modified XML
        try:
            tree.write(self._output_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
        except OSError as e:
            raise ValueError(f"Error saving output file: {e}")

    @classmethod
    def from_template(cls, template_path: str) -> 'VmXmlBuilder':
        return cls(template_path)
