import os
import asyncio
import requests
import json
import shutil
import sys
from datetime import datetime
from urllib.parse import quote
import subprocess

# 获取当前脚本的目录
script_directory = os.path.dirname(os.path.abspath(__file__ or sys.executable))

# 构建配置文件的完整路径
config_file_path = os.path.join(script_directory, 'config.json')

# 打开配置文件
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

source_path = config['sourcePath']
output_path = config['outputPath']
alist = config['alist']
token = config['token']
local_upload_directory = config['localUploadDirectory']
custom_compression_command = config['customCompressionCommand']
mode = config['mode']
upload_file_name = config['filename']
delete_output_file = config['deleteOutputFile']
delete_source_path = config['deleteSourcePath']

async def upload_and_handle_result(file_path, file_name):
    # 上传文件逻辑
    upload_url = f"{alist}/api/fs/put"
    headers = {
        'Authorization': token,
        'File-Path': quote(f'{local_upload_directory}/{file_name}')
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.put(upload_url, headers=headers, files=files)
    files['file'].close()
    
    if response.status_code == 200:
        print(f'File uploaded successfully: {response.text}')
        # 删除存放文件
        if delete_output_file:
            try:
                os.remove(file_path)
            except PermissionError as e:
                print(f'Error deleting output file: {e}')
        if delete_source_path:
            try:
                shutil.rmtree(source_path)
            except PermissionError as e:
                print(f'Error deleting source path: {e}')
    else:
        print(f'Error uploading file {file_name}: {response.text}')

if mode == 'compress_upload':
    # 执行压缩并上传操作
    # 获取当前日期和时间
    current_time = datetime.now()

    # 获取年、月、日、小时、分钟和秒
    year = current_time.strftime('%Y')
    month = current_time.strftime('%m')
    day = current_time.strftime('%d')
    hour = current_time.strftime('%H')
    minute = current_time.strftime('%M')
    second = current_time.strftime('%S')

    # 替换JSON中的变量
    custom_output_file_name = config['customOutputFileName'].format(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )

    file_name = custom_output_file_name

    # 使用自定义压缩命令，自定义的压缩命令在配置中读取
    custom_compression_command = config['customCompressionCommand'].format(outputPath=output_path, customOutputFileName=file_name, sourcePath=source_path)
    subprocess.run(custom_compression_command, shell=True)

    # 上传文件并处理结果
    upload_and_handle_result(f"{output_path}/{file_name}", file_name)

elif mode == 'direct_upload':
    if config['useLatestFile']:
  # 从配置文件中获取文件扩展名列表
        file_extensions = config['fileExtensions']
        print(file_extensions)

        # 获取文件夹中所有文件
        all_files = os.listdir(source_path)
        print(all_files)

        # 过滤出需要处理的文件
        files_to_process = [f for f in all_files if os.path.isfile(os.path.join(source_path, f)) and any(f.lower().endswith(ext) for ext in file_extensions)]
        
        print(files_to_process)

        # 创建一个字典来保存每个扩展名中最新的文件
        latest_files = {}

        for file in files_to_process:
            file_extension = os.path.splitext(file)[-1].lower()
            if file_extension not in latest_files:
                latest_files[file_extension] = file
            else:
                current_file = os.path.join(source_path, file)
                latest_file = os.path.join(source_path, latest_files[file_extension])
                if os.path.getctime(current_file) > os.path.getctime(latest_file):
                    latest_files[file_extension] = file

        # 创建事件循环
        loop = asyncio.get_event_loop()

        # 逐个上传最新文件
        for extension, latest_file in latest_files.items():
            upload_file_name = latest_file if not config['useCustomFileName'] else upload_file_name
            loop.run_until_complete(upload_and_handle_result(os.path.join(source_path, latest_file), upload_file_name))
            print(upload_file_name)

    else:
        # 上传固定文件名的文件
        upload_file_path = os.path.join(source_path, upload_file_name)

        # 上传文件并处理结果
        upload_and_handle_result(upload_file_path, upload_file_name)

else:
    print('Unsupported mode in configuration')
    exit(1)
