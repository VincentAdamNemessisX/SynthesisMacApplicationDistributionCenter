import os


# Create your tests here.
os.chdir("C:/Users/VincentAdamNemessis/Downloads/在线投稿 - MacWk_files/")
files = os.listdir()
for file in files:
    os.rename(file, file.replace(".download", ""))
print(os.listdir())