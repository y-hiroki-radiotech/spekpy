# Clinical X-ray Dosimetry Calculator

🔬 **臨床X線線量評価アプリケーション**

SpekPyライブラリを使用してESAK（Entrance Surface Air Kerma）とその他の線量評価パラメータを計算するWebアプリケーションです。

## 🎯 主な機能

- **ESAK計算**: 臨床条件に基づいた入射表面線量の評価
- **BSF補正**: 照射野サイズを考慮した後方散乱係数による線量補正
- **X線スペクトル生成**: 物理モデルに基づくスペクトルのモデリング
- **ビーム品質評価**: HVL、平均エネルギー、実効エネルギーなどの計算
- **対話的可視化**: スペクトル、線量、ビーム品質の視覚的表示
- **データエクスポート**: CSV、JSON、テキストレポート形式での結果保存
- **装置・プロトコール記録**: 装置名やプロトコール名の記録機能

## 📋 入力パラメータ

### 臨床パラメータ
- **管電圧（kVp）**: 40-150 kVp
- **管電流（mA）**: 1-1000 mA
- **照射時間（s）**: 0.001-10.0 s
- **アノード角度（°）**: 5-20°
- **線源皮膚間距離（SSD）**: 50-300 cm
- **フィルタ**: 材質（Al, Cu, Be, Air）と厚さ（mm）
- **ターゲット材質**: タングステン（W）、モリブデン（Mo）
- **照射野サイズ**: 1.0-35.0 cm（直径、BSF補正用）
- **ファントム材質**: 水（BSF計算用）

### 装置・プロトコール情報
- **装置名**: X線装置の製造会社・型番
- **プロトコール名**: 検査プロトコールの名称

## 🚀 インストールと使用方法

### 必要条件

- Python 3.8以上
- uv（Pythonパッケージ管理ツール）

### 1. 依存関係のインストール

```bash
# プロジェクトディレクトリに移動
cd clinical_xray_app

# 依存関係をインストール
uv add spekpy streamlit matplotlib pandas numpy
```

### 2. アプリケーションの起動

```bash
# Streamlitアプリを起動
streamlit run app.py
```

ブラウザでhttp://localhost:8501にアクセスしてアプリケーションを使用できます。

## 📁 プロジェクト構造

```
clinical_xray_app/
├── README.md                 # このファイル
├── app.py                   # メインStreamlitアプリケーション
├── esak_calculator.py       # ESAK計算コアモジュール
├── visualization.py         # データ可視化モジュール
├── data_export.py          # データエクスポート機能
├── simple_test.py          # 基本機能テスト
├── test_modules.py         # 包括的テスト（要依存関係）
├── pyproject.toml          # uvプロジェクト設定
├── uv.lock                 # 依存関係ロックファイル
└── exports/                # エクスポートファイル保存用（自動作成）
```

## 🔬 技術仕様

### ESAKの計算方法

1. **スペクトル生成**: SpekPyの物理モデル（kqp, casim等）を使用
2. **線量計算**: 1mAs当たりの空気カーマを基準距離（100cm）で計算
3. **距離補正**: 逆二乗法則による実際の距離での補正
4. **基本ESAK**: `ESAK = (Air Kerma/mAs) × mAs × (100cm/SSD)²`
5. **BSF補正**: `ESAK_BSF = ESAK × BSF` （照射野サイズが指定された場合）

### BSF（後方散乱係数）の計算方法

1. **データソース**: SpekPy付属のモノエネルギーBSFデータ（`monoBSFw.npz`）
2. **3D補間**: SSD、エネルギー、照射野径による補間
3. **スペクトラル重み付け**: 質量エネルギー吸収係数で重み付けした平均
4. **BSF式**: `BSF = Σ(E×Φ(E)×μen(E)×BSF(E)) / Σ(E×Φ(E)×μen(E))`

### 支援される検査タイプ

#### プリセット設定
- **胸部X線**: 120kVp, Al 2.5mm フィルタ
- **腹部X線**: 大線量設定、Al 3.0mm フィルタ
- **マンモグラフィ**: Mo ターゲット、Be + Al フィルタ

## 📊 出力結果

### 線量評価項目
- **ESAK**: mGy単位での入射表面線量
- **空気カーマ/mAs**: 基準距離での線量率
- **距離補正係数**: 逆二乗法則による補正値

### ビーム品質パラメータ
- **HVL1, HVL2**: Al、Cuでの半価層
- **平均エネルギー**: スペクトルの重み付き平均
- **実効エネルギー**: ビームの透過特性を表す等価エネルギー
- **均質度係数**: ビーム硬度の指標

## 💾 データエクスポート機能

### 対応フォーマット

1. **JSON**: 計算結果の完全なデータ
2. **CSV**:
   - サマリー形式（パラメータと結果の表）
   - スペクトルデータ（エネルギー vs フルエンス）
3. **テキストレポート**: 印刷可能な結果レポート
4. **設定ファイル**: 計算条件の再利用可能な設定

### エクスポート例

```json
{
  "metadata": {
    "export_timestamp": "2024-01-15T10:30:00",
    "software": "Clinical X-ray Dosimetry Calculator",
    "device_name": "SIEMENS Ysio Max",
    "protocol_name": "胸部正面立位"
  },
  "results": {
    "esak_mgy": 2.456,
    "hvl1_al_mm": 3.2,
    "parameters": {
      "kvp": 120,
      "mas": 10,
      "ssd_cm": 100
    }
  }
}
```

## 🧪 テストとバリデーション

### テストの実行

```bash
# 基本機能テスト（依存関係なしでも実行可能）
python simple_test.py

# 完全なテスト（全依存関係が必要）
python test_modules.py
```

### バリデーション

- SpekPyの標準テストケースとの比較
- 国際標準（NIST、BIPM、ISO）との照合
- 臨床実測値との検証

## ⚠️ 使用上の注意

### 免責事項
- **教育・研究目的**: このソフトウェアは教育と研究を目的としています
- **臨床使用**: 臨床現場での使用前に適切な品質保証手順での検証が必要です
- **精度保証**: 計算結果は必ず他の方法で検証してください

### 制限事項
- 散乱線は考慮されていません（一次線のみ）
- 患者体厚による減弱は含まれていません
- ビーム形状は均一と仮定されています

## 📚 参考文献

1. Poludniowski, G. et al. "SpekPy v2.0—a software toolkit for modeling x‐ray tube spectra." *Medical Physics* 48.7 (2021): 3630-3637.

2. Poludniowski, G. et al. "Calculating x-ray tube spectra: analytical and Monte Carlo approaches." *Medical Physics and Biomedical Engineering* (2021).

3. ICRU Report 74: "Patient Dosimetry for X Rays used in Medical Imaging" (2005).

## 🛠️ トラブルシューティング

### よくある問題

1. **SpekPy インストールエラー**
   ```bash
   # 解決方法
   uv add spekpy --timeout 600
   ```

2. **matplotlib インポートエラー**
   ```bash
   # 解決方法
   uv add matplotlib
   ```

3. **メモリ不足エラー**
   - スペクトルの分解能を下げる
   - フィルタの枚数を減らす

### ログ出力の確認

```bash
# Streamlitのデバッグモード
streamlit run app.py --logger.level debug
```

## 🤝 貢献とサポート

### 開発環境

```bash
# 開発用依存関係
uv add --dev pytest black isort mypy

# コード品質チェック
black *.py
isort *.py
mypy *.py
```

### 機能要望・バグ報告

プロジェクトのGitHubリポジトリにIssueを作成してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルを参照してください。

## 📞 お問い合わせ

技術的な質問や使用方法についてのサポートが必要な場合は、プロジェクトのドキュメントを参照いただくか、開発チームまでお問い合わせください。

---

🔬 **Clinical X-ray Dosimetry Calculator** | Built with SpekPy and Streamlit
