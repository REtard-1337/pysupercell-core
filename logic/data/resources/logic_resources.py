from typing import cast
from logic.data.string.logic_string_table import LogicStringTable
from logic.data.tables.logic_data_table_resource import LogicDataTableResource
from logic.data.tables.logic_data_tables import TABLE_COUNT, LogicDataTables
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_node import CSVNode
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicResources:
    @staticmethod
    def create_data_table_resources_array() -> LogicArrayList[LogicDataTableResource]:
        array_list = LogicArrayList[LogicDataTableResource](TABLE_COUNT)

        # Example:
        # 
        # array_list.add(
        #    LogicDataTableResource(
        #        "path/to/csv", DATA_TYPE, RESOURCE_TYPE (0 - csv, 3 - text)
        #    )
        #)

        return array_list

    @staticmethod
    def load(
        resources: LogicArrayList[LogicDataTableResource], idx: int, node: CSVNode
    ):
        resource = resources[idx]

        match resource.get_type():
            case 0:
                LogicDataTables.init_data_table(node, resource.get_table_index())
            case 3:
                LogicStringTable.create_instance(node.get_table())
            case _:
                Debugger.error("LogicResources.Invalid resource type")

        if resources.count - 1 == idx:
            LogicDataTables.create_references()
