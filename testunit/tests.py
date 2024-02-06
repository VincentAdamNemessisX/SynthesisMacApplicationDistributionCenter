import os


# Create your tests here.
os.chdir("C:/Users/VincentAdamNemessis/Downloads/Documents/软件使用 - 果核剥壳_files/")
files = os.listdir()
for file in files:
    os.rename(file, file.replace(".download", ""))
print(os.listdir())
