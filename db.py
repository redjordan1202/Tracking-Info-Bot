import gspread
from gspread.models import Worksheet

class DataStructure():
    gc = gspread.service_account()
    data_sheet = None
    db = None
    cell_last_edited = None
    row_last_edited = None
    data = None
    active_row = None

    def generate_data_structure(sheet_name,row_last_edited,):
        sheet = DataStructure.gc.open(sheet_name)
        data_sheet = sheet.get_worksheet(0)
        db = sheet.get_worksheet(1)
        DataStructure.data_sheet = data_sheet
        DataStructure.db = db
        DataStructure.row_last_edited = (
            DataStructure.data_sheet.get(row_last_edited).first()
        )
        DataStructure.active_row = int(DataStructure.row_last_edited) + 1

    def pull_data(cell):
        data = DataStructure.data_sheet.get(cell).first()
        if data != None:
            DataStructure.data = data
        else:
            DataStructure.data = '[ERR] No String Found in Given Cell'
    
    def update_last_edited():
        DataStructure.data_sheet.update_cell(2,1,DataStructure.active_row)
        

    def write_data(cell_row, cell_col, data):
        DataStructure.db.update_cell(cell_row, cell_col, data)
        DataStructure.cell_last_edited = str(str(cell_row) + str(cell_col))
        DataStructure.row_last_edited = cell_row

    def find_data(data):
        cell = DataStructure.db.find(data)
        if cell != None:
            cell_row = cell.row
            cell_col = cell.col
            return cell_row, cell_col;
        else:
            return None
        

    


