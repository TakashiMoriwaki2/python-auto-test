import pandas as pd
import re
from datetime import datetime

# 現在の年（補完用）
current_year = datetime.now().year

# CSVファイルを読み込み
df = pd.read_csv("output_deleted.csv")

# 不要な語・記号・括弧・空白を除去
def clean_date_str(s):
    if pd.isna(s):
        return ""
    s = str(s)

    # 接頭辞を削除（公演日、開催日など）
    s = re.sub(r"[［【](公演日|開催日|日程|会期|期間)[］】]?", "", s, flags=re.IGNORECASE)
    s = re.sub(r"日程[:：]?", "", s, flags=re.IGNORECASE)

    # 括弧の中の曜日などを削除
    s = re.sub(r"[（(][^)\n）]*[)）]", "", s)

    # 不要な記号を削除（文字や記号を柔らかく除去）
    s = re.sub(r"[^\d年月日./\-〜～－\s]", "", s)

    # 半角・全角スペースを正規化
    s = re.sub(r"\s+", "", s)

    return s.strip()

# 日付文字列をdatetimeに変換
def parse_date(date_str, default_year=None, default_month=None):
    date_str = clean_date_str(date_str)

    # 年月日（例: 2025年9月8日）
    match = re.search(r"(\d{4})[年./\-](\d{1,2})[月./\-](\d{1,2})", date_str)
    if match:
        y, m, d = match.groups()
    else:
        # 年.月.日 or 年/月/日
        match = re.search(r"(\d{4})[./\-](\d{1,2})[./\-](\d{1,2})", date_str)
        if match:
            y, m, d = match.groups()
        else:
            # 月日（年なし）
            match = re.search(r"(\d{1,2})[月./\-](\d{1,2})", date_str)
            if match:
                m, d = match.groups()
                y = default_year or str(current_year)
            else:
                # 日のみ（年・月を補完）
                match = re.search(r"(\d{1,2})日", date_str)
                if match and default_year and default_month:
                    d = match.group(1)
                    y = default_year
                    m = default_month
                else:
                    return None

    try:
        return datetime(int(y), int(m), int(d))
    except:
        return None

# "YYYY/MM/DD" にフォーマット
def format_date(dt):
    return dt.strftime("%Y/%m/%d") if dt else ""

# 期間表現を抽出（〜、－、- など）
def extract_start_end(date_str):
    if pd.isna(date_str):
        return "", ""

    s = clean_date_str(date_str)

    parts = re.split(r"[〜～－\-]", s)
    if len(parts) == 2:
        start_raw = parts[0].strip()
        end_raw = parts[1].strip()

        start_dt = parse_date(start_raw)
        start_y = str(start_dt.year) if start_dt else str(current_year)
        start_m = str(start_dt.month) if start_dt else "1"

        # 年省略の終了日を補完
        end_dt = parse_date(end_raw, default_year=start_y, default_month=start_m)

        # ✅ 年またぎ補正：開始月 > 終了月 かつ 終了年が明記されていない
        if start_dt and end_dt:
            if end_dt.month < start_dt.month and not re.search(r"\d{4}", end_raw):
                end_dt = end_dt.replace(year=start_dt.year + 1)

        return format_date(start_dt), format_date(end_dt)
    else:
        single_dt = parse_date(s)
        return format_date(single_dt), ""


# 結果格納用リスト
new_d_dates = []  # D列 = 開始日
new_e_dates = []  # E列 = 終了日

# 各行を処理
for d_raw, e_raw in zip(df.iloc[:, 3], df.iloc[:, 4]):
    d_str = str(d_raw)

    # D列に範囲が含まれる場合
    if re.search(r"[〜～－\-]", d_str):
        start_fmt, end_fmt = extract_start_end(d_str)
        new_d_dates.append(start_fmt)
        new_e_dates.append(end_fmt)
    else:
        # 単独日付
        d_dt = parse_date(d_raw)
        e_dt = parse_date(e_raw,
                          default_year=str(d_dt.year) if d_dt else None,
                          default_month=str(d_dt.month) if d_dt else None)

        start_fmt = format_date(d_dt)
        end_fmt = format_date(e_dt)

        # E列が空の場合、D列の値をコピー
        if not end_fmt and start_fmt:
            end_fmt = start_fmt

        new_d_dates.append(start_fmt)
        new_e_dates.append(end_fmt)

# DataFrameに反映
df.iloc[:, 3] = new_d_dates  # D列 = 開始日
df.iloc[:, 4] = new_e_dates  # E列 = 終了日



# 現在日付を取得（時刻を無視）
today = datetime.now().date()

# ① D列とE列が空でない行だけを抽出し、独立したコピーを作成
df_valid = df[(df.iloc[:, 3] != "") & (df.iloc[:, 4] != "")].copy()

# ② 終了日列をdatetimeに変換（補助列）
df_valid["終了日_date"] = pd.to_datetime(df_valid.iloc[:, 4], format="%Y/%m/%d", errors="coerce")

# ③ 今日以降のみ残す
today = datetime.now().date()
df_final = df_valid[df_valid["終了日_date"] >= pd.Timestamp(today)].copy()

# ④ 補助列を削除
df_final = df_final.drop(columns=["終了日_date"])

# 保存
df_final.to_csv("output_deleted_date.csv", index=False)

# レポート
deleted_total = len(df) - len(df_final)
print(f"✅ 終了日が空、または今日より前の行 {deleted_total} 件を削除しました。")
print("📁 完成ファイル: output_deleted_date.csv")

