# 運用ログ解析・レポート自動作成ツール

##  概要

本プロジェクトは、サーバーの運用ログをもとに、
障害傾向およびリソース使用状況を自動で分析し、
レポートとして出力・可視化するPythonツールです。

ログの集計・分析・レポート作成を自動化することで、
運用業務の効率化および品質向上を目的としています。


---

## 開発目的

- 日常運用ログ集計作業の自動化  
- 障害・異常傾向の早期発見  
- レポート作成工数の削減  
- Pythonによる実務向け開発スキルの習得  


---

## 主な機能

### ログ読込機能
- CSV / JSON形式ログ対応  
- 複数ファイル同時処理  
- フォルダ一括読込  

### データ整形・クレンジング
- 重複データ除去  
- 欠損データ除外  
- 日付形式統一  
- 不正データ除外  

### 集計・分析
- サーバー別・日別集計  
- ログレベル別件数集計（INFO / WARNING / ERROR）  
- CPU / メモリ平均値算出  
- 異常傾向分析  

### レポート出力
- Excel形式での集計結果出力  
- サーバー別シート分割  
- 日別集計一覧化  

### グラフ可視化
- CPU / メモリ使用率推移（折れ線グラフ）  
- エラー件数（棒グラフ）  
- PNG形式で保存  


---

## 使用技術

| 分類 | 技術 |
|------|------|
| 言語 | Python |
| データ処理 | Pandas |
| 可視化 | Matplotlib |
| Excel操作 | OpenPyXL |
| 管理 | Git / GitHub |


---

##  ディレクトリ構成

```text
loganalyzer/
│
├─ README.md
├─ requirements.txt
│
├─ loganalyzer/
│   ├─ __init__.py
│   ├─ analyzer.py
│   ├─ exporter.py
│   ├─ loader.py
│   ├─ logging_config.py
│   ├─ parser.py
│   └─ visualizer.py
│
├─ data/
│   ├─ input/
│   └─ output/
│
├─ logs/
│
└─ docs/
    └─ requirements.md
```


---

##  セットアップ方法

###  仮想環境作成

```bash
python -m venv venv
```

###  仮想環境有効化

#### Windows

```bash
venv\Scripts\activate
```

#### Mac / Linux

```bash
source venv/bin/activate
```

###  ライブラリインストール

```bash
pip install -r requirements.txt
```


---

##  使い方

###  ログ配置

```text
data/input/
```

###  実行

```bash
python src/main.py
```

###  出力結果

- Excelレポート：`data/output/`  
- グラフ画像：`data/output/`  


---

## 想定利用シーン

- 日次運用レポートの自動作成  
- 障害分析資料の作成  
- 運用改善データ分析  
- チーム内共有資料作成  


---

## 今後の拡張予定

- Web画面対応（Flask）
- ファイルアップロード機能
- リアルタイム分析対応
- メール通知機能追加


---

## 本プロジェクトの特徴

- 実務運用を想定した設計
- データ処理から可視化まで一貫実装
- 例外処理・ログ管理を考慮した設計
- 拡張性を意識した構成
