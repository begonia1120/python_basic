import os,time
from datetime import datetime, timedelta

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, 'backup')

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    print(f'開始模擬備份,目錄: {backup_dir}')
    print(f'按 Ctrl+C 停止並清理...' )

    try:
        while True:
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'backup_{now_str}.txt'
            filepath = os.path.join(backup_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f'Created at {now_str}\n')
            print(f'\n[+] 創建備份: {filename}')
            expire_time = now - timedelta(seconds=15)

            current_files = []
            for file in os.listdir(backup_dir):
                if file.startswith('backup_') and file.endswith('.txt'):
                    time_str = file.replace('backup_', '').replace('.txt', '')
                    file_time = datetime.strptime(time_str, '%Y-%m-%d_%H-%M-%S')
                    file_path = os.path.join(backup_dir, file)

                    if file_time < expire_time:
                        os.remove(file_path)
                        print(f'[-] 刪除過期: {file}')
                    else:
                        current_files.append(file)
            print(f'[*] 當前保留的備份 ({len(current_files)}個):')
            for f in sorted(current_files):
                print(f'    - {f}')
            time.sleep(3)
    except KeyboardInterrupt:
        print('\n\n收到停止信號，正在清理所有備份文件...')
        for file in os.listdir(backup_dir):
            if file.startswith('backup_') and file.endswith('.txt'):
                file_path = os.path.join(backup_dir, file)
                os.remove(file_path)
                print(f'[-] 已清理: {file}')
        try:
            os.rmdir(backup_dir)
            print(f'[-] 已刪除 {os.path.basename(backup_dir)} 目錄')
            print(f'清理完成，退出程序。')
        except Exception as x:
            print(f'[!] 無法刪除 {os.path.basename(backup_dir)} 目錄 (可能非空目錄)')

if __name__ == '__main__':
    main()