import io
import re
import xml.etree.ElementTree as ET
from datetime import datetime


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return formatted_date
    except (TypeError, ValueError):
        return None


def format_string(s):
    return s.strip() if s is not None else None


def remove_internal_spaces(s):
    try:
        return re.sub(r"\s+", " ", s)
    except TypeError:
        return None


class XMLTransformer:
    def __init__(self, source_xml: bytes):
        self.source_xml = source_xml

    def transform(self) -> bytes:
        parsed_xml = self._parse_xml(self.source_xml)
        transformed_xml = self._apply_transformation_rules(parsed_xml)
        return transformed_xml

    def _parse_xml(self, xml):
        source_tree = ET.parse(io.BytesIO(xml))
        source_root = source_tree.getroot()
        return source_root

    def _apply_transformation_rules(self, parsed_xml) -> bytes:
        target_root = ET.Element("InvoiceRegisters")
        target_invoices = ET.Element("Invoices")
        target_payable = ET.Element("Payable")
        target_payable.append(ET.Element("Notes"))
        target_details = ET.Element("Details")

        content = parsed_xml.find("results").find("annotation").find("content")

        for section in content:
            section_schema_id = section.get("schema_id")
            if section_schema_id == "basic_info_section":
                for datapoint in section:
                    datapoint_schema_id = datapoint.get("schema_id")
                    if datapoint_schema_id == "document_id":
                        invoice_number = ET.Element("InvoiceNumber")
                        invoice_number.text = format_string(datapoint.text)
                        target_payable.append(invoice_number)
                    if datapoint_schema_id == "date_issue":
                        invoice_date = ET.Element("InvoiceDate")
                        invoice_date.text = format_date(format_string(datapoint.text))
                        target_payable.append(invoice_date)
                    if datapoint_schema_id == "date_due":
                        due_date = ET.Element("DueDate")
                        due_date.text = format_date(format_string(datapoint.text))
                        target_payable.append(due_date)
            if section_schema_id == "basic_info_section":
                for datapoint in section:
                    datapoint_schema_id = datapoint.get("schema_id")
                    if datapoint_schema_id == "iban":
                        iban = ET.Element("Iban")
                        iban.text = format_string(datapoint.text)
                        target_payable.append(iban)

            # if section_schema_id == "invoice_info_section":
            #     for datapoint in section:
            #         datapoint_schema_id = datapoint.get("schema_id")
            #         if datapoint_schema_id == "invoice_id":
            #             invoice_number = ET.Element("InvoiceNumber")
            #             invoice_number.text = format_string(datapoint.text)
            #             target_payable.append(invoice_number)
            #         if datapoint_schema_id == "date_issue":
            #             invoice_date = ET.Element("InvoiceDate")
            #             invoice_date.text = format_date(format_string(datapoint.text))
            #             target_payable.append(invoice_date)
            #         if datapoint_schema_id == "date_due":
            #             due_date = ET.Element("DueDate")
            #             due_date.text = format_date(format_string(datapoint.text))
            #             target_payable.append(due_date)
            #         if datapoint_schema_id == "iban":
            #             iban = ET.Element("Iban")
            #             iban.text = format_string(datapoint.text)
            #             target_payable.append(iban)
            if section_schema_id == "amounts_section":
                for datapoint in section:
                    datapoint_schema_id = datapoint.get("schema_id")
                    if datapoint_schema_id == "amount_total":
                        total_amount = ET.Element("TotalAmount")
                        total_amount.text = format_string(datapoint.text)
                        target_payable.append(total_amount)
                    if datapoint_schema_id == "amount_total_tax":
                        amount = ET.Element("Amount")
                        amount.text = format_string(datapoint.text)
                        target_payable.append(amount)
                    if datapoint_schema_id == "currency":
                        curr = ET.Element("Currency")
                        curr.text = format_string(datapoint.text).upper()
                        target_payable.append(curr)
            if section_schema_id == "vendor_section":
                for datapoint in section:
                    datapoint_schema_id = datapoint.get("schema_id")
                    if datapoint_schema_id == "sender_name":
                        vendor = ET.Element("Vendor")
                        vendor.text = format_string(datapoint.text)
                        target_payable.append(vendor)
                    if datapoint_schema_id == "sender_address":
                        vendor_address = ET.Element("VendorAddress")
                        vendor_address.text = format_string(datapoint.text)
                        target_payable.append(vendor_address)
            if section_schema_id == "line_items_section":
                multivalue = section.find("multivalue")
                if multivalue is not None:
                    for tuple_ in multivalue:
                        target_detail = ET.Element("Detail")
                        target_detail.append(ET.Element("AccountId"))
                        for datapoint in tuple_:
                            datapoint_schema_id = datapoint.get("schema_id")
                            if datapoint_schema_id == "item_amount_total":
                                amount = ET.Element("Amount")
                                amount.text = format_string(datapoint.text)
                                target_detail.append(amount)
                            if datapoint_schema_id == "item_quantity":
                                quantity = ET.Element("Quantity")
                                qty = format_string(datapoint.text)
                                quantity.text = qty.upper() if qty is not None else None
                                target_detail.append(quantity)
                            if datapoint_schema_id == "item_description":
                                notes = ET.Element("Notes")
                                notes.text = format_string(
                                    remove_internal_spaces(datapoint.text)
                                )
                                target_detail.append(notes)
                        target_details.append(target_detail)

        target_payable.append(target_details)
        target_invoices.append(target_payable)
        target_root.append(target_invoices)

        return ET.tostring(target_root, encoding="utf-8", xml_declaration=True)
