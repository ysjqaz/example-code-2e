# Race condition in orignal procs.py

# 原 procs.py 中的竞态条件（race condition）

感谢读者 Michael Albert，他注意到我在 Early Release（早期预览版）期间发布的代码在 `proc.py` 中存在竞态条件（race condition）。

如果你好奇，[这个 diff](https://github.com/fluentpython/example-code-2e/commit/2c1230579db99738a5e5e6802063bda585f6476d) 展示了这个 bug 以及我是如何修复它的——但请注意，后来我把示例重构了，将 `main` 的部分职责委托给了 `start_jobs` 和 `report` 函数。

问题在于：我原本在 `jobs` 队列为空时就结束检索结果的 `while` 循环。然而，队列可能为空但仍有一些进程在运行。如果发生这种情况，就会有一个或多个结果不会被报告。我自己测试原代码时没注意到这个问题，但 Albert 演示了在 `if jobs.empty()` 这一行之前加一个 `sleep(1)` 调用就能让这个 bug 频繁出现。我采用了他的一个解决方案：让 `worker` 函数回发一个 `n = 0` 的 `PrimeResult` 作为哨兵（sentinel），以此告知主循环该进程已完成，当所有进程都结束时主循环也跟着结束。
