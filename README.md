# Paper Spider

一个用于获取来自 [Letpub](https://www.letpub.com.cn/) 的论文数据的工具。

> [!CAUTION]
> 
> 您在使用本程序时，务必注意控制访问频率，保持较长访问间隔，否则可能触发风控！
> 
> 同时，您严禁利用本程序从事一切违法犯罪行为，作者对您的非法行为概不负责！

## 使用方法

首先，安装必要的依赖

```shell
pip install .
```

随后编辑配置文件 `config.json`，其中

```json5
{
    "issnList": [
        "0162-8828", // 需要搜索的期刊或会议的 ISSN 号码
        ...
    ],
    "overwriteExistedHtml": true, // 是否覆盖已有的 HTML 网页
    "sleepInterval": 5 // 每次网络请求的间隔时间（秒）
}
```
 
程序会根据您的 `issnList` 列表逐个查询 Letpub 上的论文信息，并将对应的 HTML 网页文件保存在 `data` 文件夹。

如果 `overwriteExistedHtml` 设为 `true`，那么程序将会覆盖 `data` 文件夹下的 HTML 文件（无论文件是否存在）；如果 `overwriteExistedHtml` 设为 `false`，当对应的 HTML 文件存在时，程序将不会对应发送网络请求，而是直接从已下载的 HTML 文件中读取并分析，若文件不存在，则仍会发送网络请求。

不建议将 `sleepInterval` 调低，这可能会出现在部分查询时，服务器拒绝访问。

编辑完配置文件后，您可以运行主程序

```shell
python main.py
```

稍等片刻后，程序最终会自动输出一个 `result.json` 和一个 `result.xlsx`，这样您应该可以查看对应的论文信息了。

## Contact with Me

**Email**: AkagawaTsurunaki@outlook.com

**Github**: AkagawaTsurunaki

**Bilibili**: [赤川鹤鸣_Channel](https://space.bilibili.com/1076299680)