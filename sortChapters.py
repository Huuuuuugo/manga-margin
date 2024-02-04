import shutil
import os


prefix = 'kcc-'
zfill_size = 4
sufix = '-kcc.jpg'

path = input("Path: ").replace('\\', '/').replace('\"', '')

chapter = input("Chapter beginings: ").split()
last_page = int(input("Last page number: "))
ending = int(input("First page of the ending section (set higher than last page if none): "))
chapter_name = [None]*len(chapter)
for i, element in enumerate(chapter):
    chapter[i] = int(element)
    chapter_name[i] = input(f"Name of chapter {i+1}: ")

chapter.append(ending)

current_chapter_str = "__Início"
current_chapter = 0
page_counter = 1

try:
    os.mkdir(f"{path}/{current_chapter_str}")
except FileExistsError:
    pass 

for page in range(last_page):
    if page_counter == chapter[0]:
        if len(chapter) > 1:
            chapter.pop(0)
            current_chapter += 1
            current_chapter_str = f"{str(current_chapter).zfill(2)} - {chapter_name.pop(0)}"
        elif len(chapter) == 1:
            current_chapter_str = "Fim"

        try:
            os.mkdir(f"{path}/{current_chapter_str}")
        except FileExistsError:
            pass

    shutil.move(f"{path}/{prefix}{str(page_counter).zfill(zfill_size)}{sufix}", f"{path}/{current_chapter_str}")
    print(f"{page + 1}/{last_page}")
    page_counter += 1