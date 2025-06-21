from django.db import models
import base64
from django.contrib.auth.models import User

class Organization(models.Model):
    org_type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return "{}-{}".format(self.org_type, self.name, self.address,
                              self.address2, self.city, self.region, self.country,
                              self.digital_address, self.email)

class FuelReq(models.Model):
    date = models.DateField()
    vendor = models.CharField(max_length=100)
    po_number = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    place_of_loading = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    fuel_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    initial_tank_amount = models.DecimalField(max_digits=10, decimal_places=2)
    top_up_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    authorized_by = models.CharField(max_length=100)
    signature = models.TextField()

    def get_decoded_signature(self):
        decoded_bytes = base64.b64decode(self.signature)
        return decoded_bytes.decode('utf-8')

    def __str__(self):
        return f"{self.vendor} - {self.po_number}"

class Bill(models.Model):
    bl_number = models.CharField(max_length=20)
    shipper = models.CharField(max_length=30)
    consignee = models.CharField(max_length=30)
    notify_party = models.CharField(max_length=30)
    vessel = models.CharField(max_length=30)
    port_of_loading = models.CharField(max_length=30)
    port_of_discharge = models.CharField(max_length=10)
    container_quantity1 = models.IntegerField()
    container_type1 = models.CharField(max_length=10)
    container_quantity2 = models.IntegerField()
    container_type2 = models.CharField(max_length=10)
    package_quantity1 = models.IntegerField()
    package_type1 = models.CharField(max_length=10)
    package_quantity2 = models.IntegerField()
    package_type2 = models.CharField(max_length=10)
    kg_weight = models.DecimalField(decimal_places=2, max_digits=20)
    m3 = models.DecimalField(decimal_places=2, max_digits=20)
    container_number = models.CharField(max_length=10)

    def __str__(self):
        return "{}-{}".format(self.bl_number, self.shipper, self.consignee,
                              self.notify_party, self.vessel, self.port_of_loading, self.port_of_discharge,
                              self.container_quantity1, self.container_type1, self.container_quantity2,
                              self.container_type2, self.package_quantity1, self.package_type1, self.package_quantity2,
                              self.package_type2, self.kg_weight, self.m3, self.container_number)

class Shipment(models.Model):
    shipment_id = models.CharField(max_length=20)
    transport_mode = models.CharField(max_length=20)
    consignee = models.CharField(max_length=30)
    ata = models.DateField()
    cargo_available = models.DateField()
    date_cleared = models.DateField()
    actual_delivery = models.DateField()
    cont = models.CharField(max_length=20)
    twenty_ft = models.IntegerField()
    forty_ft = models.IntegerField()
    uw = models.CharField(max_length=10)
    weight = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return "{}-{}".format(self.shipment_id, self.consignee, self.ata,
                              self.cargo_available, self.date_cleared, self.actual_delivery,
                              self.cont, self.twenty_ft, self.forty_ft, self.uw, self.weight)

class Invoice(models.Model):
    vendor = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=20)
    client = models.CharField(max_length=100)
    client_po_number = models.CharField(max_length=20)
    invoice_date = models.DateField(max_length=30)
    currency = models.DecimalField(decimal_places=2, max_digits=20)
    goods_description = models.CharField(max_length=200)
    gross_weight = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.IntegerField()
    price_unit = models.DecimalField(decimal_places=2, max_digits=20)
    total_amount = models.DecimalField(decimal_places=2, max_digits=20)
    incoterms = models.CharField(max_length=10)

    def __str__(self):
        return "{}-{}".format(self.vendor, self.invoice_number, self.client)

class Packlist(models.Model):
    vendor = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=20)
    client = models.CharField(max_length=50)
    client_po_number = models.CharField(max_length=20)
    pack_date = models.DateField(max_length=20)
    goods_description = models.CharField(max_length=100)
    net_weight = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.IntegerField()
    hscode = models.CharField(max_length=25)

    def __str__(self):
        return "{}-{}".format(self.vendor, self.reference_number, self.client)

class Transport(models.Model):
    booking_id = models.CharField(max_length=50)
    parent_id = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    client = models.CharField(max_length=50)
    booking_req = models.CharField(max_length=50)
    first_pic_actual = models.DateField(max_length=50)
    first_pic_city = models.CharField(max_length=50)
    last_del_act = models.DateField(max_length=50)
    last_del_city = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    hazardous = models.CharField(max_length=50)
    goods_description = models.CharField(max_length=50)
    chargeable_wgt = models.DecimalField(decimal_places=2, max_digits=20)
    chargeable_wgt_unit = models.CharField(max_length=50)
    transport = models.CharField(max_length=50)
    first_pic_equipment = models.CharField(max_length=50)
    first_pick_up_cont_mode = models.CharField(max_length=50)
    first_pu_cont_type = models.CharField(max_length=50)
    consignee_package_qty = models.IntegerField()
    first_pu_pkg_type = models.CharField(max_length=50)
    first_pickup_name = models.CharField(max_length=50)
    booked_by = models.CharField(max_length=50)

    def __str__(self):
        return self.booking_id

class Waybill(models.Model):
    date = models.DateField(max_length=50)
    branch = models.CharField(max_length=50)
    client = models.CharField(max_length=50)
    booking_req = models.DateField(max_length=50)
    transport_ref = models.CharField(max_length=50)
    transport = models.CharField(max_length=50)
    booking_id = models.CharField(max_length=50)
    parent_id = models.CharField(max_length=50)
    first_pick_up_name = models.CharField(max_length=50)
    first_pic_equipment = models.CharField(max_length=50)
    first_pic_actual = models.DateField(max_length=50)
    first_pic_city = models.CharField(max_length=50)
    last_del_act = models.DateField(max_length=50)
    last_del_city = models.CharField(max_length=50)
    hazardous = models.CharField(max_length=50)
    goods_description = models.CharField(max_length=50)
    chargeable_wgt = models.DecimalField(decimal_places=2, max_digits=20)
    chargeable_wgt_unit = models.CharField(max_length=50)
    first_pic_up_cont_mode = models.CharField(max_length=50)
    first_pu_cont_type = models.CharField(max_length=50)
    consignee_package_qty = models.IntegerField()
    first_pu_pkg_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Waybill - {self.client} on {self.date.strftime('%Y-%m-%d')}"

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    department = models.CharField(max_length=50)

    class Meta:
        # User Permissions to Department Page
        permissions = [
            ("can_view_page", "View Page"),
            ("can_view_page_ops", "View Ops Page"),
            ("can_view_page_finance", "View Finance Page"),
            ("can_view_page_qhse", "View QHSE Page"),
            ("can_view_page_hr_support", "View HR Page"),
        ]

    def __str__(self):
        return self.first_name

class Pretrip(models.Model):
    driver_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    odometer_start = models.CharField(max_length=100)
    odometer_end = models.CharField(max_length=100)
    fuel_start = models.CharField(max_length=100)
    fuel_end = models.CharField(max_length=100)
    fuel_used = models.CharField(max_length=100)
    fuel_cost = models.CharField(max_length=100)
    driver_signature = models.CharField(max_length=100)
    supervisor_signature = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)

    def __str__(self):
        return self.driver_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"
