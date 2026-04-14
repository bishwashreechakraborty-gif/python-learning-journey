# write
with open("notes.txt", "w") as f:
    f.write("This is my first file.\n")

# read
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)