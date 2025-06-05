# BoidEatLine

## 実行環境
PC 上では Python 3 と pygame を用いて実行できます。

### 必要なパッケージ
- pygame
- numpy

インストール例:

```bash
pip install pygame numpy
```

### 実行方法

```bash
python main.py
```

## Requirements
外部ライブラリとして`numpy`を使用しています。Pythonista上では`scene`モジュールが標準で含まれているため追加の設定は不要ですが、
他の環境で実行する場合は以下を実行して依存パッケージをインストールしてください。

```bash
pip install -r requirements.txt
```

Pythonista以外では`scene`モジュールが存在しないため、同等のAPIを提供する環境が別途必要です。

## 使い方（Pythonista以外）
`BoidEatLine` ディレクトリで `main.py` を実行します。

```bash
python BoidEatLine/main.py
```
`scene` モジュール互換の環境が整っていない場合は正しく動作しませんのでご注意ください。

## 注意と補足
Ipad向けにパラメーターをいじっているのでiphoneの場合は個体の数が多い可能性あり。⇨SceneClass.pyのself.swarm_sizeを少なくする。

## 参考文献
このプログラムの基礎になっているBoidモデルについてはこちらなど参照⇨https://mas.kke.co.jp/model/boid-model/

Pythonistaモジュールの文書のリンクは⇨http://omz-software.com/pythonista/docs/ios/index.html
