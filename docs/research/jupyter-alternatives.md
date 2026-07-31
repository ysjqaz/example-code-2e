# PyCharm Jupyter 替代方案调研报告：能否避免写入 IDE 私有 metadata

> 调研目标：在 Windows + PyCharm 2026.2 Professional 环境下，是否存在「安装一个插件/工具即可让 `.ipynb` 不再被写入 `ExecuteTime`、`pycharm`、`vscode` 等私有 metadata」的替代方案。
>
> 调研日期：2026-07-31。

---

## 1. 结论速览（TL;DR）

1. **在 JetBrains 插件市场里，没有一个可以替代 PyCharm 内置 Jupyter 插件、同时原生支持 Python notebook 且「不写私有 metadata」的第三方插件。** 目前 JetBrains 生态中唯一面向通用 notebook 体验的官方组件就是内置的 **Python（Jupyter support）** 插件；其他官方 notebook 插件要么只支持 Kotlin（**Kotlin Notebook**，且已宣布自 IntelliJ IDEA 2026.2 起弃用），要么面向 R / Zeppelin / Big Data Tools，均不能替代 Python notebook 编辑能力。
2. **`ExecuteTime` 不是 nbformat 规范字段，而是 PyCharm/DataSpell 的私有 cell metadata**（JetBrains YouTrack 上已有 `DS-4769 PyCharm 2023.1 Release Candidate doesn't clear ExecuteTime from Jupyter Notebook metadata anymore` 等记录），目前没有官方设置可以在「保留单元格执行输出」的同时关闭持久化。Settings | Jupyter | Jupyter General 里的 `Show the timestamp on the execution label` / `Execution time display mode` 只控制 **UI 显示**，不控制是否写入文件。
3. **真正能做到「执行后 `.ipynb` 几乎零私有 metadata」的方案全部在 PyCharm 外部**，按推荐度排序：
   - **JupyterLab（不装 `jupyterlab-execute-time` 扩展）**：默认只写规范内的 `kernelspec`、`language_info`、`execution_count`、`outputs`，不写 `ExecuteTime`；`recordTiming` 是 notebook 级开关，默认关闭，只有显式装了 execute-time 扩展才会打开。
   - **nbclient / `jupyter nbconvert --to notebook --execute`**：默认会写入 `metadata.execution` 时间戳（因为 `record_timing=True`），但可以通过 `--ExecutePreprocessor.record_timing=False` / `NotebookClient(record_timing=False)` 彻底关闭，关闭后只剩 `kernelspec`、`language_info`、`execution_count`、`outputs`。
   - **marimo + `marimo export ipynb`（不带 `--include-outputs`）**：源码是 `.py`，导出的 `.ipynb` 无 outputs、无执行时间，metadata 最少。
   - **Quarto / jupytext 以 `.qmd` / `.py:percent` 为源，只在渲染/CI 时生成 `.ipynb`**：源文件本身没有 JSON metadata 污染问题。
   - **VS Code Jupyter 扩展**：仍会写 `metadata.vscode.interpreter.hash`、`orig_nbformat` 等私有字段，不是「干净」方案。
4. **最务实的组合**：继续用 PyCharm 写代码，但把 `.ipynb` 交给 **JupyterLab 浏览器界面执行 + nbstripout git filter**；或者干脆把 `02-array-seq/array-seq.ipynb` 这类以教学/演示为目的的 notebook 改造成 **jupytext `py:percent` 脚本 + `nbconvert --execute`（`record_timing=False`）** 的工作流，git 里只跟踪 `.py`。
5. **直接回答用户的问题**：「安装一个插件就解决问题」的方案 **不存在于 PyCharm 插件市场**；最接近的「一插件方案」是在 JupyterLab 端 **不安装** `jupyterlab-execute-time`（或者安装后在 Advanced Settings 里把 `recordTiming` 设回 `false`），这要求用户离开 PyCharm 内置 notebook 编辑器。

---

## 2. Notebook 文件 metadata 的「下限」（nbformat 规范）

在判断哪个工具「干净」之前，必须先明确 nbformat v4 规范本身要求什么。

来源：[The Notebook file format — nbformat 文档](https://nbformat.readthedocs.io/en/latest/format_description.html)

### 2.1 顶层必填

- `nbformat`（int，当前为 4）
- `nbformat_minor`（int）
- `metadata`（dict，可以为空 `{}`）
- `cells`（list）

### 2.2 cell 级别

任何 cell 必填：`cell_type`、`metadata`（dict，可为 `{}`）、`source`；自 nbformat 4.5 起还要求 `id`（1–64 字符，`[A-Za-z0-9_-]`）。

Code cell 额外字段：
- `execution_count`：整数或 `null`（未执行时为 `null`）
- `outputs`：list（执行后必填，但可以是 `[]`）

### 2.3 规范允许但不是「IDE 私有」的 metadata

规范列出的官方 cell metadata 包括 `collapsed`、`scrolled`、`deletable`、`editable`、`format`、`name`、`tags`，以及两个「命名空间」：
- `metadata.jupyter`（`source_hidden`、`outputs_hidden`）
- `metadata.execution`（`iopub.execute_input`、`iopub.status.busy`、`shell.execute_reply`、`iopub.status.idle` 四个 ISO 8601 时间戳）

Notebook 级别官方定义了 `kernelspec`、`authors`；`language_info` 虽未在 schema 中强制要求，但被几乎所有 kernel 在启动时写入。

### 2.4 关键结论

- `cells[].metadata` 本身可以为 `{}`，规范并不要求写入 `ExecuteTime`、`pycharm`、`vscode`、`colab` 这些字段。
- 「真正执行过」必然会让 `execution_count` 从 `null` 变成整数、`outputs` 从 `[]` 变成实际输出，并在 notebook 级别写入 `kernelspec`/`language_info`——这是规范层面的「下限」，任何工具都无法避免。
- 因此，「完全零变化」是不可能的；问题的关键只是工具会不会在这个下限之上附加 IDE 自己的字段。

nbformat 同时明确写道：「*All metadata fields are optional ... Any metadata field may also be ignored.*」并建议自定义 metadata 使用足够独特的命名空间——这正是 `ExecuteTime` / `pycharm` / `vscode` 这类字段的「合法性来源」，但也意味着工具可以选择不写。

---

## 3. PyCharm 内置 Jupyter 插件行为复盘

### 3.1 写入了哪些字段

根据用户描述及 PyCharm/DataSpell 版本说明：

- 每个 code cell 的 `metadata` 中会出现 `ExecuteTime`，包含纳秒精度的 UTC 开始/结束时间。
- `metadata.pycharm`（例如 `{"name": "#%%\n"}`）记录单元格在 percent 脚本里的分隔符等信息。
- Notebook 级别还会写入 `kernelspec`、`language_info`。

JetBrains 官方在 DataSpell 2023.1.1 的 release notes 里直接承认了 `ExecuteTime` 持久化行为，并把「PyCharm 2023.1 RC 不再清除 Jupyter Notebook metadata 里的 ExecuteTime」作为 bug `DS-4769` 修复：[DataSpell 2023.1.1 Is Out!](https://blog.jetbrains.com/dataspell/2023/05/2023-1-1/)；DataSpell 2023.1 What's New 页面也写明「the last time a code cell was executed and the duration ... are now displayed directly below the cell」：[What's New in DataSpell 2023.1](https://www.jetbrains.com/dataspell/whatsnew/2023-1/)。

### 3.2 有没有官方开关？

PyCharm 的 [Settings | Jupyter | Jupyter General](https://www.jetbrains.com/help/pycharm/jupyter.html?id=291) 中与「时间」相关的只有：

- `Show the timestamp on the execution label`
- `Execution time display mode`（detailed/compact/hide completely）
- `Notify when cell execution time exceeds 60 seconds`

这些都只控制 **UI 上是否显示**，并不会让 PyCharm 停止把 `ExecuteTime` 写入 `.ipynb`。YouTrack PY-82757 被标记为 *Answered*，即 JetBrains 明确表示不提供「关闭持久化」的开关。

### 3.3 DataSpell 也一样

DataSpell 与 PyCharm Professional 共用同一个 Jupyter 插件和 Notebook Files 核心库（见下文），因此换到 DataSpell 不会解决问题，反而同样会写 `ExecuteTime`。官方 release notes 甚至把「修复执行时间在 notebook metadata 中无法清除」当作 bugfix，说明这是被当作「特性」在维护。

---

## 4. JetBrains 生态内的替代方案

### 4.1 JetBrains Marketplace 上的 notebook 相关插件

在 plugins.jetbrains.com 上检索，与 notebook 直接相关的官方插件主要有以下几个：

| 插件 | Plugin ID | 作用 | 能否替代 PyCharm 内置 Jupyter 执行 Python notebook |
|---|---|---|---|
| [Python](https://plugins.jetbrains.com/plugin/631-python) | `Pythonid` / `com.intellij.modules.python` | 包含 **Jupyter support**，是 PyCharm Professional 写 Python notebook 的唯一官方实现 | 本身就是「肇事者」，会写 `ExecuteTime`/`pycharm` |
| [Notebook Files](https://plugins.jetbrains.com/plugin/24880-notebook-files) | `com.intellij.notebooks.core` | JetBrains 官方的共享 notebook 核心库；页面明确写着「*This plugin is a shared library ... does not provide standalone features and is not intended to be installed directly*」，需要由 Python / Kotlin Notebook / R Plugin 之一带入 | 不能单独使用 |
| [Kotlin Notebook](https://plugins.jetbrains.com/plugin/16340-kotlin-notebook) | `org.jetbrains.plugins.kotlinNotebook` | 仅支持 Kotlin；并且根据 [IntelliJ Platform SDK 文档](https://plugins.jetbrains.com/docs/intellij/tools-kotlin-notebook.html)，**Kotlin Notebook 自 IntelliJ IDEA 2026.2 起进入 sunset** | 不适用（不是 Python） |
| [R Plugin](https://plugins.jetbrains.com/plugin/10561-r) | `R4Intellij` | 仅支持 R | 不适用 |
| [Zeppelin (Big Data Tools)](https://plugins.jetbrains.com/plugin/21673-zeppelin) | `com.intellij.bigdatatools.zeppelin` | 连接 Apache Zeppelin，打开的是 Zeppelin note（`.json`），不是本地 `.ipynb` | 不适用 |

第三方插件方面，Marketplace 中没有出现任何「成熟、活跃、专门为 Python `.ipynb` 提供执行能力且明确不写私有 metadata」的插件；像 `Flexible Julia` 这类是其他语言插件，与本题无关。换言之，**JetBrains 插件市场目前没有「第二个 Python notebook 插件」可供切换**。

### 4.2 能否禁用内置 Jupyter 插件？

PyCharm 官方文档 [Managing plugins](https://www.jetbrains.com/help/pycharm/managing-plugins.html) 允许禁用任意 bundled 插件（包括 Jupyter），但：

- Jupyter 功能在 PyCharm Professional 中是 **Python 插件**的一部分；Notebook Files 是其底层依赖。
- 在 Settings | Plugins | Installed 里可以勾选掉 **Jupyter**（或 Notebook Files），重启后：
  - `.ipynb` 文件会失去 PyCharm 的 notebook 可视化编辑器，回退为纯 JSON / 文本编辑器；
  - 单元格运行按钮、变量查看器、Jupyter 控制台全部消失；
  - 你将无法在 PyCharm 内交互式执行 notebook，只能当作普通 JSON 文件编辑。
- 禁用后，Python 插件本身仍然可以运行普通 `.py` 脚本，但 notebook 体验完全消失。

因此，「禁用 Jupyter 插件 + 另装一个干净插件」在 PyCharm 里没有可落地的替代品——禁用之后要么用外部工具，要么不执行 notebook。

### 4.3 用 `.py` 脚本 + `# %%` 在 PyCharm 中执行

PyCharm 支持把 `# %%` 标记的 Python 脚本当作「Scientific mode / Python Scientific console」逐 cell 运行（[Run and debug Jupyter notebook code cells](https://www.jetbrains.com/help/pycharm/running-jupyter-notebook-cells.html) 中也提到了 `#%%` cell marker）。这种工作流的关键差异：

- **代码源是 `.py`**，根本不保存 `.ipynb`，因此不存在 notebook metadata 污染。
- PyCharm 在 SciView 中显示输出，但不会自动生成 `.ipynb`。
- 如果需要分享可执行 notebook，可在外部用 `jupytext --to notebook` 或 `nbconvert --execute` 按需生成。

这是「留在 PyCharm 内、又不污染 `.ipynb`」的最干净做法，但代价是放弃 notebook 的富文本交互（Markdown 渲染、inline 图像持久化等）。

---

## 5. 外部 notebook 编辑器/执行器对比

| 工具 | 写入的额外 metadata | 能否配置为「干净」 | 适用场景 |
|---|---|---|---|
| **JupyterLab（默认）** | notebook 级 `kernelspec`、`language_info`；code cell `execution_count`、`outputs`；默认 **不写** `metadata.execution` 时间戳，除非开启 `recordTiming` | 不安装 `jupyterlab-execute-time` 即可保持干净；如已装，在 Settings → Advanced Settings Editor → Notebook 把 `recordTiming` 设为 `false` | 主要推荐；浏览器中运行，metadata 最干净 |
| **经典 Jupyter Notebook（nbclassic）** | 同上；`ExecuteTime` 字段来自可选的 `jupyter_contrib_nbextensions` 中的 Execute Time 扩展，默认不启用 | 不启用 `execute_time` nbextension 即可 | 老版本用户 |
| **VS Code Jupyter 扩展** | 在 notebook 级写入 `metadata.vscode.interpreter.hash`、`orig_nbformat` 等字段（证据见 §6.3）；不写 `ExecuteTime`，但执行时长不会持久化 | 目前没有官方开关关闭 `vscode` metadata 写入 | 愿意换编辑器、但仍会有少量私有字段 |
| **nbclient / `jupyter nbconvert --execute`** | 默认会写 `metadata.execution.iopub.execute_input` 等时间戳（`record_timing=True`）；写入 `metadata.language_info` | `--ExecutePreprocessor.record_timing=False` 或 `NotebookClient(record_timing=False)` 可关闭；关闭后只剩规范字段 | CI、命令行、自动化执行 |
| **papermill** | 在 nbclient 基础上额外：插入一个 `tags: ["injected-parameters"]` 的新 cell；写 notebook 级 `metadata.papermill`（包含 `parameters`、`environment_variables`、`version`、`input_path`、`output_path` 等）；如果 notebook 有 `parameters` tag 才会注入 | 不参数化时不会注入 cell，但 `metadata.papermill` 仍会写入 | 参数化批量执行；不适合「干净 notebook」 |
| **marimo** | 源码是 `.py`，没有 `.ipynb` 元数据；`marimo export ipynb`（无 `--include-outputs`）生成的 `.ipynb` 无 outputs、无执行时间；`marimo convert` 从已有 ipynb 转 .py 时会 **剥离 outputs** | 天然干净（因为不以 ipynb 为源） | 愿意把 notebook 当 Python 模块写 |
| **jupytext `py:percent` paired notebook** | 把 `.py:percent` 作为 source of truth，`.ipynb` 可被 `.gitignore`；Jupyter 端保存时同步生成 `.py`，但 `.ipynb` 里写什么仍取决于你用哪个前端 | 只提交 `.py`，`.ipynb` 不入库即可彻底避开问题；如果要提交 `.ipynb`，仍需配合 nbstripout | 版本控制友好，最适合本仓库这种教学代码 |
| **Quarto（`.qmd`）** | 源文件是 Markdown + code fence；`quarto render` 可生成 `.ipynb` 但默认不执行（除非 `--execute`）；执行时使用 Jupyter 引擎，走 nbclient 路径 | 以 `.qmd` 入库即可；生成的 `.ipynb` 通常作为构建产物 | 文档/书籍/报告型 notebook |
| **Google Colab** | notebook 级写入 `metadata.colab`（`name`、`version`、`provenance`、`toc_visible`、`include_colab_link` 等）；每个 cell 写入 `id`、`colab_type`，code cell 还会写 `outputId`、`colab.base_uri`、`colab.height` | 不可关闭 | 云协作；不适合干净 git diff |
| **DeepNote / Hex / Databricks** | 各家均有自己的 notebook 级 metadata 命名空间（`deepnote`、`hex`、`dashboard metadata` 等） | 一般不可关闭 | 云平台，不适合本地仓库 |
| **Polynote / nteract / Starboard** | 各有私有 metadata（nteract 历史上写 `nteract` namespace；Polynote 使用自己的 `.ipynb` 扩展） | 基本不可关闭 | 非主流，不建议为规避 metadata 而迁移 |

---

## 6. 各方案元数据行为详细证据

### 6.1 JupyterLab 默认不写 `ExecuteTime`

- `jupyterlab-execute-time` 扩展的 PyPI 页面明确说明：「*By default, if this extension is enabled, it will automatically change your settings to record timing in the notebook metadata when it is loaded. If this fails, you can do this manually via Settings->Advanced Settings Editor->Notebook: `{"recordTiming": true}`. This is a notebook metadata setting and not a plugin setting.*」 见 [jupyterlab-execute-time 3.3.0 on PyPI](https://pypi.org/project/jupyterlab-execute-time/3.3.0/)。
- 也就是说：**时间戳写不写由 notebook 级 `recordTiming` 决定**，这个开关由 execute-time 扩展打开。不装该扩展时，JupyterLab 保持默认 `false`，不会写入。
- 上游讨论见 [jupyterlab#3320 "Add execution time to notebook/console cells"](https://github.com/jupyterlab/jupyterlab/issues/3320)，社区明确把「是否持久化时间」作为可选项讨论。

经典 Jupyter Notebook 端的 `ExecuteTime` 字段来自 `jupyter_contrib_nbextensions` 的同名扩展，文档写明「*The timing information is stored in the cell metadata, and restored on notebook load.*」见 [Execute Time — jupyter-contrib-nbextensions 文档](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/execute_time/readme.html)。默认不启用该扩展即不会写入。

### 6.2 nbclient / nbconvert 默认写 `metadata.execution`，但可关闭

- `nbclient.NotebookClient` 有一个 traitlet `record_timing: Bool = True`，文档原文：「*If True (default), then the execution timings of each cell will be stored in the metadata of the notebook.*」见 [nbclient API reference](https://nbclient.readthedocs.io/en/latest/reference/nbclient.html) 和 [deepwiki 上的 Python API 梳理](https://deepwiki.com/jupyter/nbclient/3.1-python-api)。
- 在源代码中可以看到：`if self.record_timing and 'execution' not in cell['metadata']: cell['metadata']['execution'] = {}`。
- `nbconvert.ExecutePreprocessor` 继承自 nbclient，因此同一 traitlet 可通过命令行关闭：
  ```
  jupyter nbconvert --to notebook --execute --inplace ^
    --ExecutePreprocessor.record_timing=False ^
    02-array-seq\array-seq.ipynb
  ```
  关闭后写入的字段只有规范要求的 `execution_count`、`outputs`、`kernelspec`、`language_info`。另一个可关闭的额外写入是 `--ExecutePreprocessor.store_widget_state=False`（ipywidgets 状态），见 [Executing notebooks — nbconvert 文档](https://nbconvert.readthedocs.io/en/latest/execute_api.html)。

### 6.3 VS Code Jupyter 扩展写 `vscode` 字段

- VS Code 本体在 2021 年通过 issue [#130602 "Enabling persisting notebook kernel information in notebooks"](https://github.com/microsoft/vscode/issues/130602) 和 PR #131219 引入了把 kernelspec 写回 `.ipynb` 的能力；但实际保存出的文件还包含 VS Code 自己的命名空间。
- 一个公开的样例 notebook（chroma 仓库 `examples/basic_functionality/local_persistence.ipynb`）的 notebook 级 metadata 中含有：
  ```json
  "orig_nbformat": 4,
  "vscode": {
    "interpreter": {
      "hash": "88f09714c9334832bac29166716f9f6a..."
    }
  }
  ```
  见 [raw.githubusercontent.com/.../local_persistence.ipynb](http://raw.githubusercontent.com/vochicong/chroma/0.4.9/examples/basic_functionality/local_persistence.ipynb)。
- VS Code 还存在因为 local/remote kernel 切换而删除 `language_info` 的 bug（vscode-jupyter PR "Fix notebook metadata loss when using remote Jupyter Server kernels"），侧面证明它会主动改写 metadata。
- 另一篇日文研究也指出：VS Code 的单元格执行时间显示目前 **不会** 在 `.ipynb` 中持久化（即不写类似 `ExecuteTime` 的字段），但其他 `vscode` 私有字段仍在。
- 综合结论：**VS Code 比 PyCharm 少了执行时间污染，但仍然不是零私有 metadata。**

### 6.4 papermill 写入 `papermill` namespace

- 官方文档 [Parameterize — papermill](https://papermill.readthedocs.io/en/stable/usage-parameterize.html) 说明：执行时会在带 `parameters` tag 的 cell 之后插入一个新的、tag 为 `injected-parameters` 的 cell。
- PyPI 页面 [papermill 2.7.0](https://pypi.org/project/papermill/) 同样描述了这一行为。
- papermill 还会在 notebook 级 metadata 中记录 `papermill.parameters`、`papermill.version`、`papermill.input_path`、`papermill.output_path`、`papermill.start_time`/`end_time` 等。这使得它不适合需要「干净 notebook」的场景，但它的定位是参数化批处理，本来也不是为版本控制设计的。

### 6.5 marimo：源码是 `.py`，导出 `.ipynb` 时 outputs 默认剥离

- [marimo CLI 文档](https://docs.marimo.io/cli/) 中关于 `marimo convert` 的说明：
  > Supported input formats: `.ipynb` ... Behavior: Jupyter notebooks: outputs are stripped.
- [marimo Quickstart](https://docs.marimo.io/getting_started/quickstart/) 给出了 `marimo convert your_notebook.ipynb -o your_notebook.py` 和 `marimo export ipynb notebook.py -o notebook.ipynb` 的双向命令。
- [Sharing Notebooks](https://mintlify.wiki/marimo-team/marimo/sharing-notebooks) 给出：
  ```
  marimo export ipynb notebook.py -o notebook.ipynb              # 不带 outputs
  marimo export ipynb notebook.py -o notebook.ipynb --include-outputs  # 执行并带 outputs
  ```
- 关键差异：marimo 自己的源文件是普通 Python，完全不存在 `.ipynb` metadata 污染；只有在显式导出 `.ipynb` 且加 `--include-outputs` 时才会经过 nbclient 路径写入 outputs/时间戳（此时同样可以用外部方式清洗）。

### 6.6 jupytext：用 `.py:percent` 作为 source of truth

- [Jupytext 官方文档](https://jupytext.readthedocs.io/en/latest/)：推荐 `percent` 格式，文件形如：
  ```python
  # %% [markdown]
  # This is a markdown cell

  # %%
  def f(x):
      return 3*x+1
  ```
  「*Only the notebook inputs (and optionally, the metadata) are included. Text notebooks are well suited for version control.*」
- Paired notebook 机制允许 `.ipynb` + `.py` 共存：编辑 `.py` 后在 Jupyter 里 reload，保存时再回写 `.ipynb`。官方明确建议：*You might exclude `.ipynb` files from version control ... Jupytext will recreate the `.ipynb` files locally when the users open and save the `.py` notebooks.*
- CLI 用法（[jupytext CLI](https://jupytext.org/using/cli/)）：
  - `jupytext --set-formats ipynb,py:percent notebook.ipynb`：建立配对
  - `jupytext --sync notebook.ipynb`：同步
  - `jupytext --to notebook --execute notebook.md`：转换并执行
- 对本仓库而言，最直接的做法是把 `02-array-seq/array-seq.ipynb` 配对出 `array-seq.py`，在 `.gitignore` 中忽略 `.ipynb`，git 历史从此只剩下普通 Python diff。

### 6.7 Quarto：以 `.qmd` 为源

- [Quarto JupyterLab 文档](https://quarto.org/docs/tools/jupyter-lab) 说明 Quarto 可以渲染 `.qmd` 或 `.ipynb`；默认情况下渲染 `.ipynb` 不会重新执行（「*Quarto will not execute the cells within the notebook by default*」），需要 `quarto render notebook.ipynb --execute`。
- [quarto render CLI](https://quarto.org/docs/cli/render.html) 支持 `--execute` / `--no-execute`、`--execute-daemon` 等参数。
- `quarto convert` 可以在 `.ipynb` 与 `.qmd` 之间互转。以 `.qmd` 入库后，源代码里没有 JSON metadata 污染；需要 `.ipynb` 时再由命令行生成。

### 6.8 nbstripout / nbdime 等过滤方案

如果仍希望在仓库里保留 `.ipynb`（例如需要查看渲染后的 outputs），可以配合 git filter：

- **nbstripout**（[kynan/nbstripout](https://github.com/kynan/nbstripout)，[PyPI](https://pypi.org/project/nbstripout/)）：读取 notebook → 移除 outputs 和部分 metadata → 写回，用作 git `clean` filter 或 pre-commit hook。它「*Roughly equivalent to the 'Clear All Output' command in the notebook UI, but only 'visible' to Git: keep your output in the file on disk, but don't commit the output to Git*」。安装：
  ```
  pip install nbstripout
  nbstripout --install
  ```
  可配置是否保留 `execution_count`、按大小截断 output 等；默认会 strip 掉包括 `ExecuteTime` 在内的非常规 metadata。
- **nbstripout-fast**（[deshaw/nbstripout-fast](https://github.com/deshaw/nbstripout-fast)，[PyPI](https://pypi.org/project/nbstripout-fast/)）：D. E. Shaw 用 Rust 重写的版本，在大仓库上快几十到上百倍，并支持仓库级 `.git-nbconfig.yaml` 配置要保留/剥离的字段。
- **nbdime**（[nbdime](https://nbdime.readthedocs.io/)）：提供 `nbdiff`、`nbmerge`、git 集成驱动，让 notebook diff 更可读，但不会阻止 metadata 入库，是「显示/合并」工具而非「清洗」工具。

这三者是「补救方案」，并不能让 PyCharm 不写 `ExecuteTime`，但能让写下来的字段在进入 git 时被剔除。

---

## 7. 推荐方案（按场景）

### 场景 A：必须留在 PyCharm 里、想保留交互式 notebook 体验

- **没有「换一个插件就好」的选项。** 可选项：
  1. 接受 `ExecuteTime` 写入，但在仓库中启用 **nbstripout** git filter（推荐，对工作流影响最小）。
  2. 在 Settings | Editor | File Types | Ignored Files and Folders 里把 `.ipynb` 加入忽略（JetBrains 支持在 [PyCharm modifying every notebook in repo](https://intellij-support.jetbrains.com/hc/zh-cn/community/posts/9800596213394-PyCharm-modifying-every-notebook-in-repo) 一文中给出的临时方案），这样 PyCharm 不会把这些文件当 notebook 打开——但也意味着你在 PyCharm 里失去 notebook 支持。
  3. 禁用 Jupyter 插件，在外部浏览器中打开 JupyterLab（见场景 B）。

### 场景 B：可以离开 PyCharm 内置 notebook 编辑器

- 使用 **JupyterLab**，不要安装 `jupyterlab-execute-time`；如已安装，在 Advanced Settings 中把 `recordTiming` 设回 `false`。
- 保留 PyCharm 用于普通 `.py` 编辑/调试，浏览器中跑 notebook。
- 再叠加 nbstripout，作为双保险。

### 场景 C：命令行 / CI 执行

- 用 `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.record_timing=False`，或等价的 `nbclient.NotebookClient(record_timing=False)` Python API。
- 如需参数化，papermill 仍会写 `papermill` namespace，可用 nbstripout 后处理或改用自定义 nbclient 脚本。

### 场景 D：愿意把 notebook 改写成脚本（本仓库最推荐）

- 对 `02-array-seq/array-seq.ipynb` 这类以代码为主的教学 notebook，使用 **jupytext `py:percent`**：
  1. `pip install jupytext`
  2. `jupytext --set-formats ipynb,py:percent 02-array-seq/array-seq.ipynb`
  3. 把 `.ipynb` 加入 `.gitignore`（或用 nbstripout 过滤），将 `array-seq.py` 入库
  4. 后续在 JupyterLab 里打开 `array-seq.py`（带 Notebook 图标）即可交互执行；在 PyCharm 里则当作普通 Python 脚本，用 `# %%` 分块
- 或者更进一步，改用 **marimo** / **Quarto**，从根本上不以 `.ipynb` 为 source of truth。

---

## 8. 参考来源

### nbformat 规范
- [The Notebook file format — nbformat 文档](https://nbformat.readthedocs.io/en/latest/format_description.html)
- [nbformat JSON Schema (v4)](https://github.com/jupyter/nbformat/blob/master/nbformat/v4/nbformat.v4.schema.json)

### PyCharm / DataSpell / JetBrains 插件
- [Jupyter General Settings — PyCharm Help](https://www.jetbrains.com/help/pycharm/jupyter.html?id=291)
- [运行和调试 Jupyter notebook 代码单元 — PyCharm Help 2025.2](https://www.jetbrains.com/help/pycharm/2025.2/running-jupyter-notebook-cells.html)
- [Managing Plugins — PyCharm Help](https://www.jetbrains.com/help/pycharm/managing-plugins.html)
- [Notebook Files plugin on JetBrains Marketplace](https://plugins.jetbrains.com/plugin/24880-notebook-files)
- [Kotlin Notebook plugin on JetBrains Marketplace](https://plugins.jetbrains.com/plugin/16340-kotlin-notebook)
- [Kotlin Notebook Integration — IntelliJ Platform SDK](https://plugins.jetbrains.com/docs/intellij/tools-kotlin-notebook.html)
- [Zeppelin plugin on JetBrains Marketplace](https://plugins.jetbrains.com/plugin/21673-zeppelin)
- [What's New in DataSpell 2023.1](https://www.jetbrains.com/dataspell/whatsnew/2023-1/)
- [DataSpell 2023.1.1 Is Out!（含 DS-4769 ExecuteTime 修复说明）](https://blog.jetbrains.com/dataspell/2023/05/2023-1-1/)
- [PyCharm modifying every notebook in repo — IntelliJ Support Community](https://intellij-support.jetbrains.com/hc/zh-cn/community/posts/9800596213394-PyCharm-modifying-every-notebook-in-repo)

### JupyterLab / 经典 Notebook
- [jupyterlab-execute-time on PyPI](https://pypi.org/project/jupyterlab-execute-time/3.3.0/)
- [jupyterlab#3320 Add execution time to notebook/console cells](https://github.com/jupyterlab/jupyterlab/issues/3320)
- [Execute Time — jupyter-contrib-nbextensions 文档](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/execute_time/readme.html)

### VS Code Jupyter
- [microsoft/vscode#130602 Enabling persisting notebook kernel information in notebooks](https://github.com/microsoft/vscode/issues/130602)
- [microsoft/vscode-jupyter PR: Fix notebook metadata loss when using remote Jupyter Server kernels](http://gitmemories.com/microsoft/vscode-jupyter/issues/16954)
- [Kernel Execution — vscode-jupyter Wiki](https://gh.mlsub.net/microsoft/vscode-jupyter/wiki/Kernel-Execution)
- [示例 ipynb 含 `vscode.interpreter.hash`（chroma 仓库）](http://raw.githubusercontent.com/vochicong/chroma/0.4.9/examples/basic_functionality/local_persistence.ipynb)

### nbclient / nbconvert / papermill
- [nbclient package API reference](https://nbclient.readthedocs.io/en/latest/reference/nbclient.html)
- [nbclient Python API — DeepWiki](https://deepwiki.com/jupyter/nbclient/3.1-python-api)
- [Executing notebooks — nbconvert 文档](https://nbconvert.readthedocs.io/en/latest/execute_api.html)
- [ExecutePreprocessor — nbconvert DeepWiki](https://deepwiki.com/jupyter/nbconvert/5.1-executepreprocessor)
- [Parameterize — papermill 文档](https://papermill.readthedocs.io/en/stable/usage-parameterize.html)
- [papermill on PyPI](https://pypi.org/project/papermill/)

### marimo / jupytext / Quarto
- [marimo CLI 文档](https://docs.marimo.io/cli/)
- [marimo Quickstart](https://docs.marimo.io/getting_started/quickstart/)
- [marimo Sharing Notebooks（含 `export ipynb` 用法）](https://mintlify.wiki/marimo-team/marimo/sharing-notebooks)
- [Jupytext 官方文档](https://jupytext.readthedocs.io/en/latest/)
- [Jupytext CLI](https://jupytext.org/using/cli/)
- [Quarto JupyterLab 工作流](https://quarto.org/docs/tools/jupyter-lab)
- [quarto render CLI](https://quarto.org/docs/cli/render.html)

### git filter / diff 工具
- [nbstripout on PyPI](https://pypi.org/project/nbstripout/)
- [kynan/nbstripout GitHub](https://github.com/kynan/nbstripout)
- [nbstripout-fast on PyPI](https://pypi.org/project/nbstripout-fast/)
- [nbdime 文档](https://nbdime.readthedocs.io/)
