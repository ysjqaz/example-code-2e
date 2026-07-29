# Mojifinder: Unicode character search examples

# Mojifinder：Unicode 字符搜索示例

摘自《Fluent Python, Second Edition》第 22 章「异步编程（Asynchronous Programming）」。

## 如何运行 `web_mojifinder.py`

`web_mojifinder.py` 是一个用 _[FastAPI](https://fastapi.tiangolo.com/)_ 构建的 Web 应用。
运行它之前，先安装 _FastAPI_ 和一个 ASGI 服务器。
本应用使用 _[Uvicorn](https://www.uvicorn.org/)_ 做过测试。

```
$ pip install fastapi uvicorn
```

现在可以用 `uvicorn` 启动应用了。

```
$ uvicorn web_mojifinder:app
```

最后，用浏览器访问 http://127.0.0.1:8000/ 即可看到搜索表单。


## 目录内容

下列文件可作为脚本直接从命令行运行：

- `charindex.py`：Mojifinder 示例使用的库。也可作为命令行搜索脚本使用。
- `tcp_mojifinder.py`：TCP/IP Unicode 搜索服务器。仅依赖 Python 3.9 标准库。使用 telnet 应用作为客户端。
- `web_mojifinder_bottle.py`：Unicode Web 服务。依赖 `bottle.py` 和 `static/form.html`。使用 HTTP 浏览器作为客户端。

下列程序需要 ASGI 服务器才能运行：

- `web_mojifinder.py`：Unicode Web 服务。依赖 _[FastAPI](https://fastapi.tiangolo.com/)_ 和 `static/form.html`。

辅助文件：

- `bottle.py`：单文件 _[Bottle](https://bottlepy.org/)_ Web 框架的本地副本。
- `requirements.txt`：`web_mojifinder.py` 的依赖列表。
- `static/form.html`：`web_*` 系列示例使用的 HTML 表单。
- `README.md`：本文件 🤓
