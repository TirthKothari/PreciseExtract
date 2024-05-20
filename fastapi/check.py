import os

json_groups={}
path = os.path.join("UPLOADED_FILES","80908932720233265373125914068709548619")
groups = os.listdir(path)
for g in groups:
    files_list = os.listdir(os.path.join(path,g))
    fil = []
    print(g)
    for f in files_list:
        filename , fileextension = os.path.splitext(f)
        if fileextension.casefold() in ['.jpg','.png','.pdf','.jpeg']:
            fil.append(filename)
            print(f)
    json_groups[g] = fil

print(json_groups)