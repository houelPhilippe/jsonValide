import argparse
from lxml import etree


def validate_xml(xml_path: str, xsd_path: str) -> bool:
    """Validate an XML file against an XSD schema.

    Args:
        xml_path: Path to the XML file.
        xsd_path: Path to the XSD schema file.

    Returns:
        True if the XML is valid, False otherwise.
    """
    with open(xsd_path, 'rb') as xsd_file:
        schema_doc = etree.parse(xsd_file)
        schema = etree.XMLSchema(schema_doc)

    with open(xml_path, 'rb') as xml_file:
        xml_doc = etree.parse(xml_file)

    valid = schema.validate(xml_doc)
    if not valid:
        lines: list[str]
        with open(xml_path, 'r', encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for error in schema.error_log:
            print(f"Line {error.line}, column {error.column}: {error.message}")
            if 0 < error.line <= len(lines):
                problem_line = lines[error.line - 1].rstrip("\n")
                pointer = " " * (max(error.column - 1, 0)) + "^"
                print(problem_line)
                print(pointer)
    return valid


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an XML file against an XSD schema")
    parser.add_argument("xml", help="Path to the XML file")
    parser.add_argument("xsd", help="Path to the XSD schema file")
    args = parser.parse_args()

    if validate_xml(args.xml, args.xsd):
        print("XML is valid.")
    else:
        print("XML is invalid.")
        exit(1)


if __name__ == "__main__":
    main()
