from xlrd import *
import xlsxwriter


class XLdocument:
    def __init__(self, mat, input_file, proft_path = "", loss_path = ""):
        self.wb = open_workbook(input_file)
        self.ws = self.wb.sheet_by_name('Profit and Loss')
        self.mat = mat  # materialonst
        self.wbout = None  # file for output accs
        self.profitPath = proft_path
        self.lossPath = loss_path


    def search_and_devide(self):
        saveList = []  # массив счета
        self.flag = 0  # для определения счета как loss/profit
        self.header = []  # "шапка" счетов

        # записываем даты в шапку
        for col in range(0, self.ws.ncols):
            cell = self.ws.cell(4, col)  # все ячейки дат, начиная с 5 строки
            self.header.append(cell.value)  # записали ячейку с датой

        # обработка файла
        for row in range(6, self.ws.nrows-7):  # диапазон с 7 строки
            rec = []
            for col in range(0, self.ws.ncols):
                cell = self.ws.cell(row, col)  # прочитали ячейку
                rec.append(cell.value)  # записали ячейку в массив строки

            saveList.append(rec)  # записали очередную строку в массив счета

            if len(rec[0]) - len(rec[0].strip()) == 0:
                saveList.pop(0)

            if rec[0].lower().startswith('expenses'):  # если начались "расходы", меняем флаг
                self.flag = 1

                if self.wbout is not None:  # если файл для счета существует, закрываем его и объявлем переменную пустой
                    self.wbout.close()
                    self.wbout = None
                saveList = []

            if rec[0].strip().lower().startswith('total'):  # если строка итоговая - записываем
                if len(rec[0]) - len(rec[0].strip()) < 6:  # не берем третий уровень иерархии-считаем кол-во отступов
                    if rec[-1] >= self.mat and len(saveList) > 1:   # сравниваем последний столбец с материальностью, и что счет записан
                        self.create_account(saveList, '{}'.format(row+1))
                    saveList = []


        if self.wbout is not None:
            self.wbout.close()
            self.wbout = None


    def create_account(self, data, sheetname):
        if self.flag == 0:
            bookname = self.profitPath
        else:
            bookname = self.lossPath

        if self.wbout is None:
            self.wbout = xlsxwriter.Workbook(bookname)
        ws = self.wbout.add_worksheet(sheetname)

        for col, rec in enumerate(self.header):
            ws.write(0, col, rec)

        for row, rec in enumerate(data):
            for col, val in enumerate(rec):
                ws.write(row+1, col, val)