import sys

#读取命令行参数并打印
if len(sys.argv) < 3:
    print('Need more arguements!')
else:
    print(sys.argv)
    source1 = sys.argv[1]
    source2 = sys.argv[2]
    print(source1)
    print(source2)
    
