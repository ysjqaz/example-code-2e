#!/usr/bin/env python3

from checkeddeco import checked

@checked
class Movie:
    title: str
    year: int
    box_office: float


if __name__ == '__main__':
    # 没有静态类型检查器能理解这段代码……
    movie = Movie(title='The Godfather', year=1972, box_office=137)  # type: ignore
    print(movie.title)
    print(movie)
    try:
        # 去掉 "type: ignore" 注释即可看到 Mypy 正确地发现这个错误
        movie.year = 'MCMLXXII'  # type: ignore
    except TypeError as e:
        print(e)
    try:
        # 同样，没有静态类型检查器能理解这段代码……
        blockbuster = Movie(title='Avatar', year=2009, box_office='billions')  # type: ignore
    except TypeError as e:
        print(e)
