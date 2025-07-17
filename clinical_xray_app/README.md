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

BSF（Backscatter Factor）は、ファントムからの後方散乱線による線量増加を考慮するための係数です。

#### 1. **データソース**
- **ファイル**: `9_Kilovoltage x-ray beam dosimetry/monoBSFw.npz`
- **内容**: モノエネルギーX線に対する水ファントムのBSFデータ
- **パラメータ**: SSD（40-300cm）、エネルギー（10-150keV）、照射野径（1-30cm）

#### 2. **3次元補間処理**
```python
# 3D補間関数の設定
from scipy.interpolate import RegularGridInterpolator
points = (SSD_data, Energy_data, Diameter_data)
bsf_interpolator = RegularGridInterpolator(points, BSF_data, 
                                          bounds_error=False, fill_value=1.0)

# 各エネルギーに対してBSF値を補間
for energy in spectrum_energies:
    bsf_mono = bsf_interpolator([ssd, energy, field_diameter])
```

#### 3. **スペクトラル重み付け平均**
```python
# 質量エネルギー吸収係数による重み付け
BSF = Σ(E × Φ(E) × μen(E) × BSF(E)) / Σ(E × Φ(E) × μen(E))
```

**変数説明**:
- `E`: エネルギー（keV）
- `Φ(E)`: フルエンススペクトラム（photons/cm²/keV）
- `μen(E)`: 空気の質量エネルギー吸収係数（cm²/g）
- `BSF(E)`: モノエネルギーBSF値

#### 4. **実装の詳細**

**必要なライブラリ**:
```python
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import spekpy as sp
```

**計算フロー**:
1. SpekPyでX線スペクトルを生成
2. BSFデータファイル（`monoBSFw.npz`）を読み込み
3. 3D補間関数を初期化
4. 各エネルギーに対してBSF値を補間
5. 質量エネルギー吸収係数で重み付け平均を計算
6. 最終BSF値を返す

#### 5. **典型的なBSF値**

| 照射野径 | SSD | 80kVp | 100kVp | 120kVp |
|---------|-----|-------|--------|--------|
| 5cm     | 100cm | 1.15 | 1.20 | 1.25 |
| 10cm    | 100cm | 1.25 | 1.30 | 1.35 |
| 20cm    | 100cm | 1.35 | 1.40 | 1.45 |
| 30cm    | 100cm | 1.40 | 1.45 | 1.50 |

#### 6. **BSFの物理的意味**
- **BSF = 1.0**: 後方散乱なし（狭い照射野、遠距離）
- **BSF > 1.0**: 後方散乱による線量増加
- **一般的な範囲**: 1.0 〜 1.5（臨床条件）

#### 7. **注意事項**
- 水ファントムでの計算（人体近似）
- 一次線のみの計算（散乱線は別途考慮）
- 平坦なファントム表面を仮定
- 照射野形状は円形を仮定

### 支援される検査タイプ

#### プリセット設定
- **胸部X線**: 120kVp, Al 2.5mm フィルタ
- **腹部X線**: 大線量設定、Al 3.0mm フィルタ
- **マンモグラフィ**: Mo ターゲット、Be + Al フィルタ

## 📊 出力結果

### 線量評価項目
- **IAK**: mGy単位での照射空気カーマ（BSF補正前）
- **ESAK**: mGy単位での入射表面線量（BSF補正後）
- **BSF**: 後方散乱係数（1.0〜1.5）
- **距離補正係数**: 逆二乗法則による補正値
- **BSF補正率**: 後方散乱による線量増加率（%）

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
    "esak_mgy": 1.587,
    "bsf": 1.340,
    "esak_with_bsf_mgy": 2.127,
    "hvl1_al_mm": 3.2,
    "parameters": {
      "kvp": 120,
      "mas": 10,
      "ssd_cm": 100,
      "field_size_cm": 10.0,
      "phantom_material": "water"
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
- **散乱線**: 一次線のみ計算（散乱線は別途考慮）
- **患者体厚**: 減弱は含まれていません
- **ビーム形状**: 均一と仮定
- **BSF計算**: 水ファントム、平坦表面、円形照射野を仮定
- **照射野範囲**: 1-30cm径（SpekPyデータの制限）
- **SSD範囲**: 40-300cm（SpekPyデータの制限）

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