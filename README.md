# Paper Spider

![Static Badge](https://img.shields.io/badge/Python%20-%20>=3.10-blue)

一个用于获取来自 [Letpub](https://www.letpub.com.cn/) 的论文数据的工具。

通过 ISSN 搜索对应的期刊或会议信息，可以获取期刊名、综合评分、期刊指标、学科领域、中国科学院期刊分区等信息。

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
    "nameList": [
        "ACM Transactions on Graphics", // 需要搜素的期刊或会议的名称 
        ...
    ],
    "overwriteExistedHtml": true, // 是否覆盖已有的 HTML 网页
    "sleepInterval": 10 // 每次网络请求的间隔时间（秒）
}
```
 
程序会根据您的 `issnList` 列表逐个查询 Letpub 上的论文信息，并将对应的 HTML 网页文件保存在 `data` 文件夹。

如果 `overwriteExistedHtml` 设为 `true`，那么程序将会覆盖 `data` 文件夹下的 HTML 文件（无论文件是否存在）；如果 `overwriteExistedHtml` 设为 `false`，当对应的 HTML 文件存在时，程序将不会对应发送网络请求，而是直接从已下载的 HTML 文件中读取并分析，若文件不存在，则仍会发送网络请求。

不建议将 `sleepInterval` 调到更低，这可能会出现在部分查询时，服务器拒绝访问，根据经验调整到 10 秒最合适。

编辑完配置文件后，您可以运行主程序

```shell
python main.py
```

稍等片刻后，程序最终会自动输出一个 `result.json` 和一个 `result.xlsx`，这样您应该可以查看对应的论文信息了。

## 常见问题

### 拒绝访问错误 AccessLimitError

如果在运行过程中发生了如下错误，

```
util.AccessLimitError: ⚠️ 对方服务器检测到我们已达到访问限制，建议等待较长一段时间后重试，或调整 `sleepInterval` 值到更大后重试。
```
请按照指示，然后重新运行主程序。

### 内容未找到错误 ContentNotFoundError

如果在运行过程中发生了如下错误，

```
😭 期刊/会议名为 {searchname} 的内容未找到，请检查您输入的名称后重试：`journalid` 为 null
```

这意味着，你配置文件中指定的 `nameList` 列表中存在某个期刊/会议名称无法在 [Letpub](https://www.letpub.com.cn/) 上查询到，建议自行到官网手动查询，有可能是大小写的问题，或者包含了 & 符号，或者是带有 and 之类的字样干扰了搜索引擎。

如果在运行过程中发生了如下错误，

```
😭 ISSN 为 {searchissn} 的内容未找到，请检查您的 ISSN 后重试：`journalid` 为 null
```

这意味着，你配置文件中指定的 `issnList` 列表中存在某个 ISSN 无法在 [Letpub](https://www.letpub.com.cn/) 上查询到，建议自行到官网手动查询，一般是混淆了 ISSN (print) 和 ISSN (online) 两个号。

## Contact with Me

**Email**: AkagawaTsurunaki@outlook.com

**Github**: AkagawaTsurunaki

**Bilibili**: [赤川鹤鸣_Channel](https://space.bilibili.com/1076299680)