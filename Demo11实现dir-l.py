import os, time
demopath = r'C:/Users/rog/Desktop/Demo'

def dir_l(path):
    filenum, filesize, dirnum = 0, 0, 0
    for i in os.listdir(path):
        i = os.path.join(path, i)
        #os.listdir(i)只会列出i下的文件和目录名称，因此要用os.path.join(a,b,c)把a,b,c连接在一起返回绝对路径
        mtime = time.strftime("%Y-%m-%d  %H:%M", time.localtime(os.path.getmtime(i)))
        #os.path.getmtime(name) 获得name文件的最后修改的时间（时间戳）
        #time.localtime() 将Timestamp对象转换为struct_time对象
        #strftime()将struct_time对象转换为格式化时间
        if os.path.isfile(i):
            size = os.path.getsize(i)
            print('%s\t\t%d\t%s' %(mtime, size, i))
            filenum += 1
            filesize += size
        if os.path.isdir(i):
            print('%s\t<DIR>\t%s' %(mtime, i))
            dirnum += 1
    print('\t\t%d个文件\t%d个字节' %(filenum, filesize))
    print('\t\t%d个目录' %dirnum)

if __name__ == '__main__':
    dir_l(demopath)