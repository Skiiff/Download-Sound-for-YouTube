import checking_identical
import converting_txt_csv
import download
while(1):
    print("-"*68)
    print("1. Для конвертации txt файла в csv введите 1;", "2. Для объединения csv файлов без дубликатов введите 2;"\
          ,"3. Для загрузки из файла с названием 'final_file.csv' введите 3;","4. для того чтобы выйти введите любой другой символ;",sep="\n")
    print("-"*68)
    comands = str(input(">>>"))
    if comands == "1":
        converting_txt_csv.run()
    elif comands == "2":
        checking_identical.run()
    elif comands == "3":
        download.run()

    else:
        print(">your exit<")
        break