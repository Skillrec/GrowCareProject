class Device:
    def __init__(self, id, name, mac_address=None):
        self.name = name
        self.mac_address = mac_address
        self.id = id

    def set_mac_address(self, mac_address):
        self.mac_address = mac_address

    def get_mac_address(self):
        return self.mac_address

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def __str__(self):
        return 'ID: ' + self.id + ' Name: ' + self.name + ' MAC-ADDRESS: ' + self.mac_address
