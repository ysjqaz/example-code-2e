#!/usr/bin/env python3

"""下载按人口排名前 20 位国家的国旗

使用 ``as_completed`` 的 ThreadPoolExecutor 示例。
"""
from concurrent import futures

from flags import main
from flags_threadpool import download_one


# tag::FLAGS_THREADPOOL_AS_COMPLETED[]
def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]  # <1>
    with futures.ThreadPoolExecutor(max_workers=3) as executor:  # <2>
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):  # <3>
            future = executor.submit(download_one, cc)  # <4>
            to_do.append(future)  # <5>
            print(f'Scheduled for {cc}: {future}')  # <6>

        for count, future in enumerate(futures.as_completed(to_do), 1):  # <7>
            res: str = future.result()  # <8>
            print(f'{future} result: {res!r}')  # <9>

    return count
# end::FLAGS_THREADPOOL_AS_COMPLETED[]

if __name__ == '__main__':
    main(download_many)
