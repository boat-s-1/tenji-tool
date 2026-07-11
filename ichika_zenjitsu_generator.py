from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"


def file_to_data_url(path: str | Path) -> str:
    file_path = Path(path)

    if not file_path.is_absolute():
        file_path = BASE_DIR / file_path

    if not file_path.exists() or not file_path.is_file():
        return ""

    mime_type, _ = mimetypes.guess_type(file_path.name)
    mime_type = mime_type or "application/octet-stream"

    encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def public_path_to_data_url(value: str) -> str:
    if not value:
        return ""

    if value.startswith("data:image/"):
        return value

    parsed = urlparse(value)
    raw_path = unquote(parsed.path or value).lstrip("/")

    if raw_path.startswith("bsc/"):
        return file_to_data_url(ASSET_DIR / raw_path)

    return ""


def safe_text(value: Any) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


def clamp(value: Any, minimum: int, maximum: int, default: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default

    return max(minimum, min(maximum, number))


def create_ichika_html(data: dict[str, Any]) -> str:
    race_date = safe_text(data.get("raceDate"))
    place = safe_text(data.get("place"))
    race_no = safe_text(data.get("raceNo"))
    honmei = safe_text(data.get("honmei"))
    stamp = safe_text(data.get("stamp"))

    nige_rate = clamp(data.get("nigeRate"), 0, 100, 0)
    up_rate = clamp(data.get("upRate"), -30, 30, 0)
    wave = clamp(data.get("wave"), 0, 100, 0)

    main_comment = safe_text(data.get("mainComment"))
    danger_boat = safe_text(data.get("dangerBoat"))
    motor_eval = safe_text(data.get("motorEval"))

    selected_boats = [
        str(item)
        for item in data.get("selectedBoats", [])
        if str(item) in {"1", "2", "3", "4", "5", "6"}
    ]

    boat_scores = {
        str(key): value
        for key, value in (data.get("boatScores") or {}).items()
    }

    boat_comments = {
        str(key): value
        for key, value in (data.get("boatComments") or {}).items()
    }

    character_src = (
        public_path_to_data_url(str(data.get("characterImage") or ""))
        or file_to_data_url(
            "assets/bsc/characters/ichika/797e612d-792c-4bc6-ba4a-2ea3d2db6103.png"
        )
    )

    background_src = public_path_to_data_url(
        str(data.get("backgroundImage") or "")
    )

    header_src = (
        background_src
        or file_to_data_url("assets/bsc/newspaper/ichika/header.png")
    )

    footer_src = file_to_data_url(
        "assets/bsc/newspaper/common/footer.png"
    )

    boat_images = {
        str(index): file_to_data_url(
            f"assets/bsc/newspaper/boats/boat-{index}.png"
        )
        for index in range(1, 7)
    }

    boat_colors = {
        "1": "#eeeeee",
        "2": "#333333",
        "3": "#ff4b4b",
        "4": "#2875e8",
        "5": "#ffc107",
        "6": "#28a745",
    }

    story_parts: list[str] = []

    for boat in sorted(selected_boats, key=int):
        comment = safe_text(boat_comments.get(boat, ""))
        image_src = boat_images.get(boat, "")
        color = boat_colors.get(boat, "#ff4f93")

        icon_html = (
            f'<img src="{image_src}" alt="">'
            if image_src
            else f'<span class="boat-chip" style="background:{color}">{boat}</span>'
        )

        story_parts.append(
            f"""
            <div class="story-item" style="border-left-color:{color}">
                {icon_html}
                <div>
                    <strong>{boat}号艇</strong>
                    <p>{comment or "展開コメント未入力"}</p>
                </div>
            </div>
            """
        )

    graph_parts: list[str] = []

    for boat in ["1", "2", "3", "4", "5", "6"]:
        score = clamp(boat_scores.get(boat), 0, 100, 50)
        color = boat_colors[boat]

        graph_parts.append(
            f"""
            <div class="score-item">
                <div class="score-label">
                    <span>{boat}号艇</span>
                    <b>{score}</b>
                </div>
                <div class="score-track">
                    <div class="score-bar" style="width:{score}%;background:{color}"></div>
                </div>
            </div>
            """
        )

    story_html = "".join(story_parts)
    graph_html = "".join(graph_parts)
    stars = "★" * max(1, min(5, wave // 20 + 1))
    up_rate_text = f"+{up_rate}%" if up_rate > 0 else f"{up_rate}%"

    header_html = (
        f'<img src="{header_src}" alt="">'
        if header_src
        else '<div class="header-fallback">一果ちゃん新聞</div>'
    )

    footer_html = (
        f'<img src="{footer_src}" alt="">'
        if footer_src
        else '<strong>BOAT STRIKE</strong>'
    )

    regular_font = file_to_data_url("fonts/NotoSansJP-Regular.ttf")
    bold_font = file_to_data_url("fonts/NotoSansJP-Bold.ttf")

    return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1000">
<style>
@font-face {{ font-family:"NotoSansJP"; src:url("{regular_font}"); font-weight:400; }}
@font-face {{ font-family:"NotoSansJP"; src:url("{bold_font}"); font-weight:700 900; }}
* {{ box-sizing:border-box; }}
html, body {{ width:1100px; margin:0; padding:0; background:#fff; font-family:"NotoSansJP","Noto Sans CJK JP",sans-serif; }}
.wrapper {{ width:1000px; margin:0; overflow:hidden; border:6px dashed #ff6ea8; border-radius:25px; background:#fffdf5; }}
.header {{ position:relative; width:1000px; height:150px; overflow:hidden; border-bottom:5px dashed #ff6ea8; background:#fff; }}
.header > img {{ position:absolute; inset:0; width:1000px; height:150px; object-fit:cover; }}
.header-fallback {{ position:absolute; inset:0; display:flex; align-items:center; padding-left:35px; background:linear-gradient(135deg,#fff,#ffe6f0); color:#ff4f93; font-size:38px; font-weight:900; }}
.race-info {{ position:absolute; top:18px; right:30px; z-index:2; text-align:right; }}
.race-date {{ color:#333; font-size:23px; font-weight:700; }}
.race-title {{ display:flex; align-items:baseline; justify-content:flex-end; gap:13px; }}
.race-title strong {{ color:#ff4f93; font-size:50px; }}
.race-title span {{ color:#333; font-size:43px; font-weight:700; }}
.main {{ display:grid; grid-template-columns:610px 330px; gap:20px; padding:20px; }}
.panel {{ margin-bottom:18px; padding:18px; border:4px dashed #ffb3cf; border-radius:22px; background:#fff; }}
.section-title {{ display:inline-block; margin-bottom:14px; padding:5px 14px; border-radius:7px; background:#ff4f93; color:#fff; font-size:23px; font-weight:700; }}
.main-boat {{ color:#ff4f93; font-size:33px; font-weight:700; }}
.rate-row {{ display:flex; align-items:baseline; justify-content:space-between; margin-top:14px; padding-bottom:10px; border-bottom:3px dashed #ffd0e2; }}
.rate-row span {{ color:#333; font-size:20px; font-weight:700; }}
.rate-row strong {{ color:#ff4f93; font-size:78px; line-height:1; }}
.rate-row small {{ font-size:28px; }}
.diff-row {{ display:flex; align-items:center; justify-content:space-between; padding-top:12px; }}
.diff-row span {{ color:#666; font-size:18px; }}
.diff-row strong {{ color:#44aa55; font-size:32px; }}
.story-item {{ display:flex; align-items:flex-start; gap:12px; margin-bottom:11px; padding:11px; border-left:8px solid; border-radius:12px; background:#f8f8f8; }}
.story-item img {{ width:62px; height:48px; flex-shrink:0; object-fit:contain; }}
.boat-chip {{ width:50px; height:50px; display:grid; place-items:center; flex-shrink:0; border-radius:50%; color:#fff; font-size:22px; font-weight:900; }}
.story-item strong {{ color:#222; font-size:17px; }}
.story-item p {{ margin:4px 0 0; color:#444; font-size:14px; line-height:1.5; }}
.score-item {{ margin-bottom:10px; }}
.score-label {{ display:flex; justify-content:space-between; margin-bottom:4px; color:#333; font-size:15px; font-weight:700; }}
.score-label b {{ color:#ff4f93; }}
.score-track {{ height:23px; overflow:hidden; border:1px solid #ddd; border-radius:14px; background:#eee; }}
.score-bar {{ height:100%; }}
.character {{ width:100%; height:370px; display:block; object-fit:contain; }}
.speech {{ position:relative; margin-top:-45px; padding:19px; border:4px solid #ff6ea8; border-radius:24px; background:#fff; }}
.speech h3 {{ margin:0 0 8px; color:#ff4f93; font-size:19px; text-align:center; }}
.speech p {{ margin:0; color:#333; font-size:16px; line-height:1.6; }}
.notice {{ margin-top:18px; padding:14px; border:4px dashed #ff6ea8; border-radius:18px; background:#fff3c4; color:#333; font-size:15px; line-height:1.8; }}
.motor {{ margin-top:18px; padding:14px; border:3px solid #7ec2ff; border-radius:15px; background:#f0f9ff; }}
.motor h3 {{ margin:0 0 8px; color:#0875c1; font-size:17px; text-align:center; }}
.motor p {{ margin:0; color:#333; font-size:15px; line-height:1.6; }}
.footer {{ min-height:100px; padding:18px; color:#ff4f93; text-align:center; font-size:28px; }}
.footer img {{ width:900px; max-height:150px; object-fit:contain; }}
</style>
</head>
<body>
<div class="wrapper" id="newspaper">
  <header class="header">
    {header_html}
    <div class="race-info">
      <div class="race-date">{race_date}</div>
      <div class="race-title"><strong>{place}</strong><span>{race_no}R</span></div>
    </div>
  </header>
  <main class="main">
    <section>
      <div class="panel">
        <div class="section-title">本命候補</div>
        <div class="main-boat">{honmei}号艇</div>
        <div class="rate-row"><span>イン逃げ期待度</span><strong>{nige_rate}<small>%</small></strong></div>
        <div class="diff-row"><span>場平均との差</span><strong>{up_rate_text}</strong></div>
      </div>
      <div class="panel"><div class="section-title">展開ストーリー</div>{story_html}</div>
      <div class="panel"><div class="section-title">各艇評価指数</div>{graph_html}</div>
    </section>
    <aside>
      <img class="character" src="{character_src}" alt="">
      <div class="speech"><h3>🌸 一果のひとこと</h3><p>{main_comment}</p></div>
      <div class="notice">波乱指数：{stars}（{wave}）<br>危険艇：{"なし" if danger_boat == "なし" else f"{danger_boat}号艇"}<br>スタンプ：{stamp}</div>
      <div class="motor"><h3>一果の機力チェック</h3><p>{motor_eval}</p></div>
    </aside>
  </main>
  <footer class="footer">{footer_html}</footer>
</div>
</body>
</html>
"""
