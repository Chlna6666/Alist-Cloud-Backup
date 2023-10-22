# Alist-Cloud-Backup
通过Alist-API 实现上传云端

```
{
  "mode": "direct_upload",  // 上传模式，可以是 "direct_upload" 或 "compress_upload" direct_upload可以直接上传 compress_upload需要压缩上传
  "sourcePath": "D:\\Users\\Desktop\\12321321\\新建文件夹",  // 源文件夹的路径
  "outputPath": "D:\\Users\\Desktop\\12321321",  // 输出文件夹的路径
  "alist": "http://127.0.0.1:5244",  // Alist 云端备份服务的地址
  "token": "alist-114514",  // 授权令牌
  "fileExtensions": [".7z", ".zip"],  // 允许上传的文件扩展名列表（direct_upload）
  "localUploadDirectory": "alist/1",  // 上传到alist的目录
  "customOutputFileName": "文件名{year}-{month}-{day}-{hour}-{minute}-{second}.zip",  // 自定义输出文件名模板（两个模式通用）
  "useCustomFileName": false,  // 是否使用自定义文件名（两个模式通用）
  "filename": "中文y12.zip",  // 文件名（direct_upload下的指定文件上传）
  "useLatestFile": true,  // 是否使用最新文件（direct_upload）
  "customCompressionCommand": "powershell Compress-Archive -Path '{sourcePath}' -DestinationPath '{outputPath}/{customOutputFileName}'",  // 自定义压缩命令（compress_upload）
  "deleteOutputFile": false,  // 是否删除输出文件（compress_upload）
  "deleteSourcePath": false  // 是否删除源文件夹（compress_upload）
}

```
### 部分功能没有实现

## TODO
- 多线程上传
- compress_upload支持多文件夹上传
- 支持上传多个路径
