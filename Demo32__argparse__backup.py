#用argparse解析关键字参数和位置参数
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog= 'Backup',
        description= 'Backup MySQL database.',
        epilog= 'Copyright(r) 2023' #epilogue结尾信息
    )
    parser.add_argument('outfile')  #定义位置参数
    
    parser.add_argument('--host', default= 'localhost') #定义关键字参数主机名/IP
    parser.add_argument('--port', default= 3306, type= int) #定义MySQL的端口号，参数必须为int类型
    #定义用户
    parser.add_argument('-u', '--user', required= True) #其中规定缩写是'-'，全称是'--'
    parser.add_argument('-p', '--password', required= True)
    parser.add_argument('--database', required= True)
    #gz参数不需要保存参数值，因此action= 'store_true'出现就将parser.gz保存为True  (gz压缩)
    parser.add_argument('-gz', '--gzcompress', action= 'store_true', required= False, help= 'Compress backup files by gz')
    
    args = parser.parse_args()  #从命令行解析参数返回一个NameSpace对象，可以引用调用数据
    
    print('parsed args:')
    print(f'outfile = {args.outfile}')
    print(f'host = {args.host}')
    print(f'port = {args.port}')
    print(f'user = {args.user}')
    print(f'password = {args.password}')
    print(f'database = {args.database}')
    print(f'gzcompress = {args.gzcompress}')

if __name__ == '__main__':
    main()
    
#示例输入：python Demo32__argparse__backup.py output.sql --user myuser --password mypassword --database mydb --host localhost --port 3301    