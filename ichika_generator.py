from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent


def file_to_data_url(path: str | Path) -> str:
    file_path = Path(path)

    if not file_path.is_absolute():
        file_path = BASE_DIR / file_path

    if not file_path.exists():
        return ""

    mime_type, _ = mimetypes.guess_type(file_path.name)
    mime_type = mime_type or "application/octet-stream"

    encoded = base64.b64encode(
        file_path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def safe_text(value: Any) -> str:
    return html.escape(str(value or ""))


def create_ichika_html(data: dict[str, Any]) -> str:
    race_date = safe_text(data.get("raceDate"))
    place = safe_text(data.get("place"))
    race_no = safe_text(data.get("raceNo"))

    honmei = safe_text(data.get("honmei"))
    stamp = safe_text(data.get("stamp"))

    nige_rate = int(data.get("nigeRate", 0))
    up_rate = int(data.get("upRate", 0))
    wave = int(data.get("wave", 0))

    main_comment = safe_text(
        data.get("mainComment")
    )

    danger_boat = safe_text(
        data.get("dangerBoat")
    )

    motor_eval = safe_text(
        data.get("motorEval")
    )

    selected_boats = data.get(
        "selectedBoats",
        [],
    )

    boat_scores = data.get(
        "boatScores",
        {},
    )

    boat_comments = data.get(
        "boatComments",
        {},
    )

    character_src = data.get(
        "characterImage"
    ) or file_to_data_url(
        "images/ichika/ichika-01.png"
    )

    logo_src = file_to_data_url(
        "images/ichika/header.png"
    )

    footer_src = file_to_data_url(
        "images/common/footer.png"
    )

    boat_images = {
        "1": file_to_data_url(
            "images/boats/boat-1.png"
        ),
        "2": file_to_data_url(
            "images/boats/boat-2.png"
        ),
        "3": file_to_data_url(
            "images/boats/boat-3.png"
        ),
        "4": file_to_data_url(
            "images/boats/boat-4.png"
        ),
        "5": file_to_data_url(
            "images/boats/boat-5.png"
        ),
        "6": file_to_data_url(
            "images/boats/boat-6.png"
        ),
    }

    boat_colors = {
        "1": "#eeeeee",
        "2": "#333333",
        "3": "#ff4b4b",
        "4": "#2875e8",
        "5": "#ffc107",
        "6": "#28a745",
    }

    story_html = ""

    for boat in sorted(
        selected_boats,
        key=lambda value: int(value),
    ):
        boat_key = str(boat)
        comment = safe_text(
            boat_comments.get(
                boat_key,
                "",
            )
        )

        image_src = boat_images.get(
            boat_key,
            "",
        )

        color = boat_colors.get(
            boat_key,
            "#ff4f93",
        )

        story_html += f"""
        <div class="story-item"
             style="border-left-color:{color}">
            <img src="{image_src}" alt="">
            <div>
                <strong>{boat_key}号艇</strong>
                <p>{comment}</p>
            </div>
        </div>
        """

    graph_html = ""

    for boat in ["1", "2", "3", "4", "5", "6"]:
        score = int(
            boat_scores.get(boat, 50)
        )

        color = boat_colors[boat]

        graph_html += f"""
        <div class="score-item">
            <div class="score-label">
                <span>{boat}号艇</span>
                <b>{score}</b>
            </div>

            <div class="score-track">
                <div class="score-bar"
                     style="
                       width:{score}%;
                       background:{color};
                     ">
                </div>
            </div>
        </div>
        """

    stars = "★" * max(
        1,
        min(5, wave // 20 + 1),
    )

    up_rate_text = (
        f"+{up_rate}%"
        if up_rate > 0
        else f"{up_rate}%"
    )

    return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">

<style>
@font-face {{
    font-family: "NotoSansJP";
    src: url(
      "{file_to_data_url('fonts/NotoSansJP-Bold.ttf')}"
    );
    font-weight: 700;
}}

@font-face {{
    font-family: "NotoSansJP";
    src: url(
      "{file_to_data_url('fonts/NotoSansJP-Regular.ttf')}"
    );
    font-weight: 400;
}}

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    padding: 0;
    width: 1100px;
    background: #ffffff;
    font-family: "NotoSansJP", sans-serif;
}}

.wrapper {{
    width: 1000px;
    margin: 0;
    background: #fffdf5;
    border: 6px dashed #ff6ea8;
    border-radius: 25px;
    overflow: hidden;
}}

.header {{
    position: relative;
    width: 1000px;
    height: 150px;
    border-bottom: 5px dashed #ff6ea8;
    background: #fff;
}}

.header img {{
    position: absolute;
    inset: 0;
    width: 1000px;
    height: 150px;
    object-fit: cover;
}}

.race-info {{
    position: absolute;
    top: 18px;
    right: 30px;
    z-index: 2;
    text-align: right;
}}

.race-date {{
    font-size: 23px;
    font-weight: 700;
}}

.race-title {{
    display: flex;
    gap: 13px;
    align-items: baseline;
    justify-content: flex-end;
}}

.race-title strong {{
    font-size: 50px;
    color: #ff4f93;
}}

.race-title span {{
    font-size: 43px;
    font-weight: 700;
}}

.main {{
    display: grid;
    grid-template-columns: 610px 330px;
    gap: 20px;
    padding: 20px;
}}

.panel {{
    margin-bottom: 18px;
    padding: 18px;
    border: 4px dashed #ffb3cf;
    border-radius: 22px;
    background: #fff;
}}

.section-title {{
    display: inline-block;
    margin-bottom: 14px;
    padding: 5px 14px;
    border-radius: 7px;
    background: #ff4f93;
    color: #fff;
    font-size: 23px;
    font-weight: 700;
}}

.main-boat {{
    font-size: 33px;
    font-weight: 700;
    color: #ff4f93;
}}

.rate-row {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-top: 14px;
    padding-bottom: 10px;
    border-bottom: 3px dashed #ffd0e2;
}}

.rate-row span {{
    font-size: 20px;
    font-weight: 700;
}}

.rate-row strong {{
    color: #ff4f93;
    font-size: 78px;
    line-height: 1;
}}

.rate-row small {{
    font-size: 28px;
}}

.diff-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
}}

.diff-row span {{
    font-size: 18px;
    color: #666;
}}

.diff-row strong {{
    font-size: 32px;
    color: #44aa55;
}}

.story-item {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 11px;
    padding: 11px;
    border-left: 8px solid;
    border-radius: 12px;
    background: #f8f8f8;
}}

.story-item img {{
    width: 62px;
    height: 48px;
    object-fit: contain;
    flex-shrink: 0;
}}

.story-item strong {{
    font-size: 17px;
}}

.story-item p {{
    margin: 4px 0 0;
    font-size: 14px;
    line-height: 1.5;
    color: #444;
}}

.score-item {{
    margin-bottom: 10px;
}}

.score-label {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 15px;
    font-weight: 700;
}}

.score-label b {{
    color: #ff4f93;
}}

.score-track {{
    height: 23px;
    overflow: hidden;
    border: 1px solid #ddd;
    border-radius: 14px;
    background: #eee;
}}

.score-bar {{
    height: 100%;
}}

.character {{
    width: 100%;
    height: 370px;
    object-fit: contain;
    display: block;
}}

.speech {{
    position: relative;
    margin-top: -45px;
    padding: 19px;
    border: 4px solid #ff6ea8;
    border-radius: 24px;
    background: #fff;
}}

.speech h3 {{
    margin: 0 0 8px;
    color: #ff4f93;
    font-size: 19px;
    text-align: center;
}}

.speech p {{
    margin: 0;
    font-size: 16px;
    line-height: 1.6;
}}

.notice {{
    margin-top: 18px;
    padding: 14px;
    border: 4px dashed #ff6ea8;
    border-radius: 18px;
    background: #fff3c4;
    font-size: 15px;
    line-height: 1.8;
}}

.motor {{
    margin-top: 18px;
    padding: 14px;
    border: 3px solid #7ec2ff;
    border-radius: 15px;
    background: #f0f9ff;
}}

.motor h3 {{
    margin: 0 0 8px;
    color: #0875c1;
    text-align: center;
    font-size: 17px;
}}

.motor p {{
    margin: 0;
    font-size: 15px;
    line-height: 1.6;
}}

.footer {{
    padding: 18px;
    text-align: center;
}}

.footer img {{
    width: 900px;
    max-height: 150px;
    object-fit: contain;
}}
</style>
</head>

<body>
<div class="wrapper" id="newspaper">
    <header class="header">
        <img src="{logo_src}" alt="">

        <div class="race-info">
            <div class="race-date">
                {race_date}
            </div>

            <div class="race-title">
                <strong>{place}</strong>
                <span>{race_no}R</span>
            </div>
        </div>
    </header>

    <main class="main">
        <section>
            <div class="panel">
                <div class="section-title">
                    本命候補
                </div>

                <div class="main-boat">
                    {honmei}号艇
                </div>

                <div class="rate-row">
                    <span>イン逃げ期待度</span>
                    <strong>
                        {nige_rate}
                        <small>%</small>
                    </strong>
                </div>

                <div class="diff-row">
                    <span>場平均との差</span>
                    <strong>
                        {up_rate_text}
                    </strong>
                </div>
            </div>

            <div class="panel">
                <div class="section-title">
                    展開ストーリー
                </div>

                {story_html}
            </div>

            <div class="panel">
                <div class="section-title">
                    各艇評価指数
                </div>

                {graph_html}
            </div>
        </section>

        <aside>
            <img
              class="character"
              src="{character_src}"
              alt=""
            >

            <div class="speech">
                <h3>🌸 一果のひとこと</h3>
                <p>{main_comment}</p>
            </div>

            <div class="notice">
                波乱指数：{stars}（{wave}）<br>
                危険艇：
                {
                    "なし"
                    if danger_boat == "なし"
                    else f"{danger_boat}号艇"
                }<br>
                スタンプ：{stamp}
            </div>

            <div class="motor">
                <h3>一果の機力チェック</h3>
                <p>{motor_eval}</p>
            </div>
        </aside>
    </main>

    <footer class="footer">
        <img src="{footer_src}" alt="">
    </footer>
</div>
</body>
</html>
"""
