[ja](./README.ja.md)

# Tsv2HtmlTable

Convert TSV to HTML table tag.

# DEMO

* [demo](https://ytyaru.github.io/Python.Tsv2HtmlTable.20201022074246/)

<table><tr><th rowspan="3" colspan="3"></th><th colspan="4">ア</th><th rowspan="3">イ</th><th>ウ</th><th></th></tr><tr><th colspan="2">A</th><th colspan="2">B</th><th></th><th rowspan="2">C</th></tr><tr><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr><tr><th rowspan="4">あ</th><th rowspan="2">A</th><th>a</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td></tr><tr><th>b</th><td>H</td><td>I</td><td>J</td><td>K</td><td>L</td><td>M</td><td>N</td></tr><tr><th rowspan="2">B</th><th>c</th><td>OP</td><td></td><td>QX</td><td>R</td><td>STZa</td><td></td><td>U</td></tr><tr><th>d</th><td>V</td><td>W</td><td></td><td>Y</td><td></td><td></td><td>b</td></tr><tr><th colspan="3">い</th><td>c</td><td>d</td><td>e</td><td>f</td><td>g</td><td>h</td><td>i</td></tr><tr><th>う</th><th></th><th>e</th><td>j</td><td>k</td><td>l</td><td>m</td><td>n</td><td>o</td><td>p</td></tr><tr><th></th><th colspan="2">C</th><td>q</td><td>r</td><td>s</td><td>t</td><td>u</td><td>v</td><td>w</td></tr></table>

# Requirement

* <time datetime="2020-10-22T07:42:30+0900">2020-10-22</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspbian](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2019-09-26 <small>[setup](http://ytyaru.hatenablog.com/entry/2019/12/25/222222)</small>
* bash 5.0.3(1)-release
* Python 2.7.16
* Python 3.7.3
* [pyxel][] 1.3.1

[pyxel]:https://github.com/kitao/pyxel

```sh
$ uname -a
Linux raspberrypi 5.4.51-v7l+ #1333 SMP Mon Aug 10 16:51:40 BST 2020 armv7l GNU/Linux
```

# Usage

```sh
git clone https://github.com/ytyaru/Python.Tsv2HtmlTable.20201022074246
cd Python.Tsv2HtmlTable.20201022074246
cat docs/tsv/matrix_3.tsv | src/tsv2table.py
```

## CLI

```sh
tsv2table.py [-H a|r|c|m] [-r t|b|B] [-c l|r|B]
```

<table>
    <tr>
            <th>短</th><th>長</th><th>初期値</th><th>候補値</th>
    </tr>
    <tr>
            <td><code>-H</code></td><td><code>--header</code></td><td><code>a</code></td><td>
                <table>
                <tr><td><code>a</code></td><td><code>auto</code></td><td>ヘッダを推測する。<small><br>1行目1列目が空でなければ列ヘッダなし。<br>1行目に空がなければ行ヘッダは1行のみ。</small></td></tr>
                <tr><td><code>r</code></td><td><code>row</code></td><td>行ヘッダがある。</td></tr>
                <tr><td><code>c</code></td><td><code>column</code></td><td>列ヘッダがある。</td></tr>
                <tr><td><code>m</code></td><td><code>matrix</code></td><td>行列ヘッダがある。</td></tr>
                </table>
            </td>
    </tr>
    <tr>
            <td><code>-r</code></td><td><code>--row</code></td><td><code>t</code></td><td>
                <table>
                <tr><td><code>t</code></td><td><code>top</code></td><td>行ヘッダを上端に配置する。</td></tr>
                <tr><td><code>b</code></td><td><code>bottom</code></td><td>行ヘッダを下端に配置する。</td></tr>
                <tr><td><code>B</code></td><td><code>both</code></td><td>行ヘッダを上下両端に配置する。</td></tr>
                </table>
            </td>
    </tr>
    <tr>
            <td><code>-c</code></td><td><code>--column</code></td><td><code>l</code></td><td>
                <table>
                <tr><td><code>l</code></td><td><code>left</code></td><td>列ヘッダを左端に配置する。</td></tr>
                <tr><td><code>r</code></td><td><code>right</code></td><td>列ヘッダを右端に配置する。</td></tr>
                <tr><td><code>B</code></td><td><code>both</code></td><td>列ヘッダを左右両端に配置する。</td></tr>
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

