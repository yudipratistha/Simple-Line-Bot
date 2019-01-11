
str = "cari mahasiswa #nama #prodi"
print(str.replace("#nama", "#"+ "aaaaaaa"))

str1 = "SELECT * FROM mahasiswa WHERE nama LIKE '%?%' AND prodi LIKE '%?%'"
a = str1.find("?")
print(a)


i=+