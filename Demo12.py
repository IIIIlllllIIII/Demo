import os
demopath = r'C:/Users/rog/Desktop/Demo'

def search(text, path):
    if not isinstance(text, str):
        raise TypeError('Please input str')


    for name in os.listdir(path):
        real_path = os.path.join(path, name)
        if os.path.isdir(real_path):
            search(text, real_path)
        else:
            if name.find(text) != -1:
                print(name,'\t', os.path.relpath(real_path, demopath))
                #relpath\(relative_path\)(root, start)是指获取从start到root的相对路径       
       
if __name__ == '__main__':
    search('Demo2', demopath)
