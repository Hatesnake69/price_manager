import openpyxl


def fill_kaspi_goods(file_path):
    # Открываем файл
    workbook = openpyxl.load_workbook(file_path)
    # Получаем первый лист
    sheet = workbook.active

    # Проходим по строкам и столбцам листа

    counter = 0
    for row in sheet.iter_rows(values_only=True):
        print(row)
        counter += 1
        if counter == 5:
            break


if __name__ == "__main__":
    fill_kaspi_goods("Ledvisionkz_6682e12720359f0131c9fba0.xlsx")
