from typing import List, Optional

from logic.data.core.global_id import GlobalID
from logic.data.core.logic_data import LogicData
from logic.data.tables.logic_data_table import LogicDataTable
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_node import CSVNode


TABLE_COUNT = 52


class LogicDataTables:
    _tables: List[Optional[LogicDataTable]] = [None] * TABLE_COUNT

    @staticmethod
    def init():
        LogicDataTables._tables = [None] * TABLE_COUNT

    @staticmethod
    def init_data_table(node: CSVNode, index: LogicDataType):
        table_data = node.get_table()
        if LogicDataTables._tables[index] is not None:
            table = LogicDataTables._tables[index]
            assert isinstance(table, LogicDataTable)
            table.set_table(table_data)
        else:
            if index == LogicDataType.GLOBAL:
                pass
            else:
                LogicDataTables._tables[index] = LogicDataTable(table_data, index)

    @staticmethod
    def create_references():
        for i in range(TABLE_COUNT):
            if LogicDataTables._tables[i]:
                table = LogicDataTables._tables[i]
                assert isinstance(table, LogicDataTable)
                table.create_references()

        LogicDataTables.gold_data = LogicDataTables.get_resource_by_name("Gold", None)
        LogicDataTables.elixir_data = LogicDataTables.get_resource_by_name(
            "Elixir", None
        )

    @staticmethod
    def get_table(table_index: LogicDataType) -> Optional[LogicDataTable]:
        return LogicDataTables._tables[table_index]

    @staticmethod
    def get_data_by_id(global_id: int) -> Optional[LogicData]:
        table_index = GlobalID.get_class_id(global_id) - 1

        if (
            table_index >= 0
            and table_index < TABLE_COUNT
            and LogicDataTables._tables[table_index] != None
        ):
            table = LogicDataTables._tables[table_index]
            if table:
                return table.get_item_by_id(global_id)
        return None

    @staticmethod
    def get_data_by_id_typed(
        global_id: int, data_type: LogicDataType
    ) -> Optional[LogicData]:
        data = LogicDataTables.get_data_by_id(global_id)
        if data and data.get_data_type() == data_type:
            return data
        return None

    @staticmethod
    def get_data_by_name(
        name: str, data_type: LogicDataType, caller: Optional[LogicData]
    ) -> Optional[LogicData]:
        table = LogicDataTables._tables[data_type]
        assert isinstance(table, LogicDataTable)

        return table.get_data_by_name(name, caller)