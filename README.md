[ja](./README.ja.md)

# Tsv2HtmlTable

Convert TSV to HTML table tag.

# DEMO

* [demo](https://ytyaru.github.io/Python.Tsv2HtmlTable.20201022074246/)

<table><tr><th rowspan="3" colspan="3"></th><th colspan="4">ア</th><th rowspan="3">イ</th><th>ウ</th><th></th></tr><tr><th colspan="2">A</th><th colspan="2">B</th><th></th><th rowspan="2">C</th></tr><tr><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr><tr><th rowspan="4">あ</th><th rowspan="2">A</th><th>a</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td></tr><tr><th>b</th><td>H</td><td>I</td><td>J</td><td>K</td><td>L</td><td>M</td><td>N</td></tr><tr><th rowspan="2">B</th><th>c</th><td>OP</td><td></td><td>QX</td><td>R</td><td>STZa</td><td></td><td>U</td></tr><tr><th>d</th><td>V</td><td>W</td><td></td><td>Y</td><td></td><td></td><td>b</td></tr><tr><th colspan="3">い</th><td>c</td><td>d</td><td>e</td><td>f</td><td>g</td><td>h</td><td>i</td></tr><tr><th>う</th><th></th><th>e</th><td>j</td><td>k</td><td>l</td><td>m</td><td>n</td><td>o</td><td>p</td></tr><tr><th></th><th colspan="2">C</th><td>q</td><td>r</td><td>s</td><td>t</td><td>u</td><td>v</td><td>w</td></tr></table>

# Requirement

* <time datetime="2020-10-22T07:42:30+0900">2020-10-22</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspberry Pi OS](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2020-08-20 <small>[setup](http://ytyaru.hatenablog.com/entry/2020/10/06/111111)</small>
* bash 5.0.3(1)-release
* Python 3.7.3

```sh
$ uname -a
Linux raspberrypi 5.4.51-v7l+ #1333 SMP Mon Aug 10 16:51:40 BST 2020 armv7l GNU/Linux
```

# Usage

```sh
git clone https://github.com/ytyaru/Python.Tsv2HtmlTable.20201022074246
cd Python.Tsv2HtmlTable.20201022074246
cat ./docs/tsv/matrix_3.tsv | ./src/tsv2table.py
```

## CLI

```sh
tsv2table.py [-H a|r|c|m] [-r t|b|B] [-c l|r|B]
```

<table>
    <tr>
            <th>short</th><th>long</th><th>default</th><th>values</th>
    </tr>
    <tr>
            <td><code>-H</code></td><td><code>--header</code></td><td><code>a</code></td><td>
                <table>
                <tr><td><code>a</code></td><td><code>auto</code></td><td>Guess the header.<small><br>If the first row and first column are not empty, there is no column header.<br>If there is no space in the first line, there is only one line header.</small></td></tr>
                <tr><td><code>r</code></td><td><code>row</code></td><td>There is a line header.</td></tr>
                <tr><td><code>c</code></td><td><code>column</code></td><td>There is a column header.</td></tr>
                <tr><td><code>m</code></td><td><code>matrix</code></td><td>There is a matrix header.</td></tr>
                </table>
            </td>
    </tr>
    <tr>
            <td><code>-r</code></td><td><code>--row</code></td><td><code>t</code></td><td>
                <table>
                <tr><td><code>t</code></td><td><code>top</code></td><td>Place the row header at the top.</td></tr>
                <tr><td><code>b</code></td><td><code>bottom</code></td><td>Place the line header at the bottom.</td></tr>
                <tr><td><code>B</code></td><td><code>both</code></td><td>Place line headers at the top and bottom ends.</td></tr>
                </table>
            </td>
    </tr>
    <tr>
            <td><code>-c</code></td><td><code>--column</code></td><td><code>l</code></td><td>
                <table>
                <tr><td><code>l</code></td><td><code>left</code></td><td>Place the column header on the far left.</td></tr>
                <tr><td><code>r</code></td><td><code>right</code></td><td>Place the column header on the far right.</td></tr>
                <tr><td><code>B</code></td><td><code>both</code></td><td>Place column headers on the left and right ends.</td></tr>
                </table>
            </td>
    </tr>
</table>

# Author

ytyaru

* [![github](http://www.google.com/s2/favicons?domain=github.com)](https://github.com/ytyaru "github")
* [![hatena](http://www.google.com/s2/favicons?domain=www.hatena.ne.jp)](http://ytyaru.hatenablog.com/ytyaru "hatena")
* [![mastodon](http://www.google.com/s2/favicons?domain=mstdn.jp)](https://mstdn.jp/web/accounts/233143 "mastdon")

# License

This software is CC0 licensed.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.en)

