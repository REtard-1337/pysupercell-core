from logic.data.core.global_id import GlobalID
from logic.data.core.logic_data import LogicData
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_table import CSVTable
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicDataTable:
    def __init__(self, table: CSVTable, index: LogicDataType) -> None:
        self.table = table
        self.table_idx = index
        self.items = LogicArrayList[LogicData | None]()
        self.is_loaded = False
        self.table_name = ""

        self.load_tables()

    def load_tables(self) -> None:
        for i in range(self.table.get_row_count()):
            self.items.add(self.create_item(self.table.get_row_at(i)))

    def create_references(self) -> None:
        if not self.is_loaded:
            for item in self.items:
                assert item is not None
                item.create_references()
            self.is_loaded = True

    def get_item_at(self, index: int) -> LogicData | None:
        return self.items[index]

    def set_table(self, table: CSVTable) -> None:
        self.table = table
        for i, item in enumerate(self.items):
            assert item is not None
            item.set_row(table.get_row_at(i))

    def set_name(self, name: str) -> None:
        self.table_name = name

    def get_item_count(self) -> int:
        return self.items.count

    def get_item_by_id(self, global_id: int) -> LogicData | None:
        instance_id = GlobalID.get_instance_id(global_id)
        if 0 <= instance_id < self.items.count:
            return self.items[instance_id]
        Debugger.warning("LogicDataTable.get_item_by_id() - Instance id out of bounds!")
        return None

    def get_data_by_name(self, name: str, caller: LogicData | None) -> LogicData | None:
        if name:
            for data in self.items:
                assert data is not None
                if data.get_name() == name:
                    return data

            if caller:
                Debugger.warning(
                    f"CSV row ({caller.get_name()}) has an invalid reference ({name})"
                )

        return None

    def get_table_name(self) -> str:
        return self.table_name

    def create_item(self, row) -> LogicData | None:
        item = None

        match self.table_idx:
            case _:
                Debugger.error(f"Invalid data table id: {self.table_idx}")

        return item

    def get_table_index(self) -> LogicDataType:
        return self.table_idx
