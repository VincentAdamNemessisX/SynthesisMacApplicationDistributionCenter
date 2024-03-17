import os


# Create your tests here.
os.chdir("C:/Users/VincentAdamNemessis/Downloads/Documents/test")
files = os.listdir()
for file in files:
    os.rename(file, file.replace(".download", ""))
print(os.listdir())
