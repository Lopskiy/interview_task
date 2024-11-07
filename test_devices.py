#!/usr/bin/env python
###################################################################
# network_device_test.py : Test script to verify the functionality 
#                          of NetworkDevice, Router, and Switch classes.
###################################################################

import os
import logging
from pyats import aetest
from classes import NetworkDevice, Router, Switch 

# Set up logging
log = logging.getLogger(__name__)

log_directory = os.path.join('.', 'logs')
log_file = os.path.join(log_directory, 'network_devices.log')
os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(filename=log_file, filemode='w', encoding='utf-8', level=logging.INFO)

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section for initializing devices """

    @aetest.subsection
    def initialize_devices(self):
        """ Initialize the devices to be tested """
        log.info("Initializing NetworkDevice, Router, and Switch")

        # Create instances of NetworkDevice, Router, and Switch for testing
        self.parent.parameters['device'] = NetworkDevice(name="Device1", ip_address="192.168.1.1")
        self.parent.parameters['router'] = Router(name="Router1", ip_address="10.0.0.1")
        self.parent.parameters['switch'] = Switch(name="Switch1", ip_address="172.16.0.1")

###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class TestNetworkDevice(aetest.Testcase):
    """ Testcase for NetworkDevice """

    @aetest.setup
    def setup(self, device):
        """ Testcase Setup for NetworkDevice """
        log.info("Setting up NetworkDevice test case")
        device.power_off()

    @aetest.test
    def test_power_on_off(self, device):
        """ Test power on/off functionality """
        device.power_on()
        assert device.status is True, "Power on failed"
        log.info("Device powered on successfully")

        device.power_off()
        assert device.status is False, "Power off failed"
        log.info("Device powered off successfully")

    @aetest.test
    def test_get_info(self, device):
        """ Test the get_info method """
        expected_info = "Device: Device1 \nIP Address: 192.168.1.1 \nStatus: Non Active \n"
        assert device.get_info() == expected_info, "Get info output does not match expected"
        log.info("Device info retrieved successfully")

class TestRouter(aetest.Testcase):
    """ Testcase for Router """

    @aetest.setup
    def setup(self, router):
        """ Testcase Setup for Router """
        log.info("Setting up Router test case")
        router.power_on()

    @aetest.test
    def test_add_route(self, router):
        """ Test adding routes """
        router.add_route(destination="192.168.2.0", gateway="10.0.0.2")
        assert "192.168.2.0" in router.routing_table, "Route addition failed"
        log.info("Route added successfully")

    @aetest.test
    def test_remove_route(self, router):
        """ Test removing routes """
        router.add_route(destination="192.168.3.0", gateway="10.0.0.3")
        router.remove_route(destination="192.168.3.0")
        assert "192.168.3.0" not in router.routing_table, "Route removal failed"
        log.info("Route removed successfully")

class TestSwitch(aetest.Testcase):
    """ Testcase for Switch """

    @aetest.setup
    def setup(self, switch):
        """ Testcase Setup for Switch """
        log.info("Setting up Switch test case")
        switch.power_on()

    @aetest.test
    def test_create_vlan(self, switch):
        """ Test creating VLAN """
        switch.create_vlan(vlan_id=100)
        assert switch.vlan == 100, "VLAN creation failed"
        log.info("VLAN created successfully")

    @aetest.test
    def test_delete_vlan(self, switch):
        """ Test deleting VLAN """
        switch.create_vlan(vlan_id=200)
        switch.delete_vlan(vlan_id=200)
        assert switch.vlan is None, "VLAN deletion failed"
        log.info("VLAN deleted successfully")

#####################################################################
####                       COMMON CLEANUP SECTION                 ###
#####################################################################

class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for network device tests """

    @aetest.subsection
    def cleanup_devices(self, device, router, switch):
        """ Common Cleanup for devices """
        device.power_off()
        router.power_off()
        switch.power_off()
        log.info("All devices powered off")

if __name__ == '__main__':
    result = aetest.main()
    aetest.exit_cli_code(result)
