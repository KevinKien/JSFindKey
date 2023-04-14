import argparse
import os
import requests
import yaml
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description='Kiểm tra các file js có chứa thông tin nhạy cảm')
    parser.add_argument('url', help='URL của trang web cần kiểm tra')
    parser.add_argument('--yaml', default='rules.yaml', help='Đường dẫn đến file yaml chứa các rules kiểm tra')
    args = parser.parse_args()

    url = args.url
    yaml_path = args.yaml

    # Tải về trang web và trích xuất các file js
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

    # Kiểm tra từng file js xem có chứa thông tin nhạy cảm hay không
    with open(yaml_path, 'r') as f:
        rules = yaml.safe_load(f)

    sensitive_info = []
    for js_file in js_files:
        file_path = os.path.join(os.getcwd(), js_file)
        with open(file_path, 'r') as f:
            content = f.read()
        for rule in rules:
            if rule['regex'] in content:
                sensitive_info.append((js_file, rule['name']))
                break

    # Hiển thị kết quả thông tin nhạy cảm
    if sensitive_info:
        print('Các thông tin nhạy cảm phát hiện được là:')
        for info in sensitive_info:
            print(f'- Trong file {info[0]} có chứa thông tin {info[1]}')
    else:
        print('Không có thông tin nhạy cảm phát hiện được')


if __name__ == '__main__':
    main()
