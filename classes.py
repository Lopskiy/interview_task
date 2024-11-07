import logging

# Set up logging
log = logging.getLogger(__name__)


class NetworkDevice:
    def __init__(self, name: str, ip_address: str) -> None:
        self.name = name
        self.ip_address = ip_address
        self.status = False # Выключенно по умолчанию
    
    def power_on(self) -> None:
        self.status = True
        log.info(f'{self.name} is on')

    def power_off(self) -> None:
        self.status = False
        log.info(f'{self.name} is off')  

    def get_info(self) -> str:
        status_str = 'Active' if self.status else 'Non Active'
        return f'Device: {self.name} \nIP Address: {self.ip_address} \nStatus: {status_str} \n'

class Router(NetworkDevice):
    def __init__(self, name: str, ip_address: str) -> None:
        super().__init__(name, ip_address)
        self.routing_table = {}
    
    def add_route(self, destination: str, gateway: str) -> None:
        self.routing_table[destination] = gateway
        log.info(f'Added route {destination}: {gateway} on {self.name}')
    
    def remove_route(self, destination: str) -> None:
        if destination in self.routing_table:
            del self.routing_table[destination]
            log.info(f'Route {destination} removed from {self.name}')
        else:
            log.info(f'Route {destination} not found on {self.name}')

    def get_info(self) -> str:
        base_info =  super().get_info()
        routing_info = f'Routing Table: {self.routing_table}\n'
        return base_info + routing_info
    
class Switch(NetworkDevice):
    def __init__(self, name: str, ip_address: str) -> None:
        super().__init__(name, ip_address)
        self.vlan = None

    def create_vlan(self, vlan_id: int) -> None:
        self.vlan = vlan_id
        log.info(f'VLAN {vlan_id} created on {self.name}')

    def delete_vlan(self, vlan_id: int) -> None:
        if self.vlan == vlan_id:
            self.vlan = None
            log.info(f'VLAN {vlan_id} deleted on {self.name}')
        else:
            log.info(f'VLAN {vlan_id} not found on {self.name}')
                      
    def get_info(self) -> str:
        base_info =  super().get_info()
        vlan_info = f'VLAN: {self.vlan}\n' if self.vlan else 'VLAN: None\n'
        return base_info + vlan_info