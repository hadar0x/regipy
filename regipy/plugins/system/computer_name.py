import logbook

from regipy.exceptions import RegistryValueNotFoundException
from regipy.hive_types import SYSTEM_HIVE_TYPE
from regipy.plugins.plugin import Plugin
from regipy.utils import convert_wintime

logger = logbook.Logger(__name__)

COMPUTER_NAME_PATH = r'Control\ComputerName\ComputerName'


class ComputerNamePlugin(Plugin):
    NAME = 'computer_name'
    DESCRIPTION = 'Get the computer name'
    COMPATIBLE_HIVE = SYSTEM_HIVE_TYPE

    def run(self):
        logger.info('Started Computer Name Plugin...')

        computer_names = []
        for subkey_path in self.registry_hive.get_control_sets(COMPUTER_NAME_PATH):
            subkey = self.registry_hive.get_key(subkey_path)

            try:
                computer_name = subkey.get_value('ComputerName', as_json=self.as_json)
                computer_names.append({
                    'name': computer_name.value,
                    'timestamp': convert_wintime(subkey.header.last_modified, as_json=self.as_json)
                })
            except RegistryValueNotFoundException as ex:
                continue
        return computer_names

