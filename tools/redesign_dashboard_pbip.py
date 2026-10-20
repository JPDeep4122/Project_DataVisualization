import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "dashboard" / "Dashboard_Custom.Report"
PAGES = REPORT / "definition" / "pages"

OVERVIEW = "a1ab8509b3eee61b13ac"
TREND = "26f15efa213e2c3971bb"
COUNTRY = "6f6c64e831bf4200c0af"
DETAIL = "4d268b666f82860db6e3"
FORECAST = "f9be36e28695a86d10af"

NAVY = "#0E4F5C"
NAVY_DARK = "#146F70"
MOVIE_BLUE = "#126B87"
SHOW_TEAL = "#43B7A3"
TEAL = SHOW_TEAL
AMBER = "#3C9198"
OFF_WHITE = "#EDF7F5"
TEXT = "#183F46"
KPI_SURFACE = "#F2FAF8"
KPI_BORDER = "#A8D8D0"
KPI_VALUE = "#126B78"
TITLE_BAND = "#DDF1EE"
TITLE_DIVIDER = "#9AD4CB"
NAV_SELECTED = "#B7E8DF"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def visual_path(page, visual_id):
    return PAGES / page / "visuals" / visual_id / "visual.json"


def set_position(page, visual_id, x, y, width, height):
    path = visual_path(page, visual_id)
    data = read(path)
    data["position"].update({"x": x, "y": y, "width": width, "height": height})
    write(path, data)


def set_shape_fill(page, visual_id, color):
    path = visual_path(page, visual_id)
    data = read(path)
    fills = data.get("visual", {}).get("objects", {}).get("fill", [])
    if fills:
        expr = fills[0]["properties"]["fillColor"]["solid"]["color"]["expr"]
        expr.clear()
        expr["Literal"] = {"Value": f"'{color}'"}
    write(path, data)


def set_textbox(page, visual_id, value=None, font_size=None, x=None, y=None, width=None, height=None):
    path = visual_path(page, visual_id)
    data = read(path)
    pos = data.get("position", {})
    for key, val in (("x", x), ("y", y), ("width", width), ("height", height)):
        if val is not None:
            pos[key] = val
    visual = data.get("visual", {})
    paragraphs = visual.get("objects", {}).get("general", [{}])[0].get("properties", {}).get("paragraphs", [])
    if value is not None and paragraphs:
        paragraphs[0]["textRuns"] = [{"value": value, "textStyle": {
            "fontWeight": "bold", "fontFamily": "Segoe UI", "fontSize": f"{font_size or 38}pt", "color": "#ffffff"
        }}]
        paragraphs[0]["horizontalTextAlignment"] = "center"
        # Preserve a subtitle when the title box has one; reset it to a restrained size.
        for paragraph in paragraphs[1:]:
            for run in paragraph.get("textRuns", []):
                style = run.setdefault("textStyle", {})
                style.update({"fontFamily": "Segoe UI", "fontSize": "15pt", "color": "#DCE7F1"})
    elif font_size is not None and paragraphs:
        for paragraph in paragraphs:
            for run in paragraph.get("textRuns", []):
                style = run.setdefault("textStyle", {})
                style["fontFamily"] = "Segoe UI"
                style["fontSize"] = f"{font_size}pt"
                style.setdefault("fontWeight", "bold")
                style["color"] = "#ffffff"
    write(path, data)


def style_overview_header():
    path = visual_path(OVERVIEW, "160616b075e9bb9f632b")
    data = read(path)
    paragraphs = data["visual"]["objects"]["general"][0]["properties"]["paragraphs"]
    for run in paragraphs[0].get("textRuns", []):
        run["textStyle"].update({"fontFamily": "Segoe UI", "fontSize": "38pt", "fontWeight": "bold", "color": "#ffffff"})
    for run in paragraphs[1].get("textRuns", []):
        run["textStyle"].update({"fontFamily": "Segoe UI", "fontSize": "15pt", "color": "#DCE7F1"})
    write(path, data)


def set_nav(page, nav_id, welcome_id, sidebar_id):
    set_position(page, sidebar_id, 0, 120, 280, 1320)
    set_shape_fill(page, sidebar_id, NAVY_DARK)
    set_position(page, welcome_id, 0, 135, 280, 84)
    path = visual_path(page, welcome_id)
    data = read(path)
    run = data["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
    run["textStyle"].update({"fontFamily": "Segoe UI", "fontSize": "26pt", "color": "#ffffff"})
    data["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["horizontalTextAlignment"] = "center"
    write(path, data)
    set_position(page, nav_id, 0, 235, 280, 790)
    path = visual_path(page, nav_id)
    data = read(path)
    for item in data.get("visual", {}).get("objects", {}).get("text", []):
        props = item.get("properties", {})
        props["fontFamily"] = {"expr": {"Literal": {"Value": "'''Segoe UI'''"}}}
        props["fontSize"] = {"expr": {"Literal": {"Value": "16D"}}}
    write(path, data)


def tidy_shape(page, visual_id):
    path = visual_path(page, visual_id)
    data = read(path)
    vc = data.setdefault("visualContainerObjects", {})
    vc["border"] = [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "radius": {"expr": {"Literal": {"Value": "12D"}}},
        "width": {"expr": {"Literal": {"Value": "1D"}}},
    }}]
    vc["dropShadow"] = [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "shadowSpread": {"expr": {"Literal": {"Value": "0D"}}},
        "shadowBlur": {"expr": {"Literal": {"Value": "3D"}}},
        "shadowDistance": {"expr": {"Literal": {"Value": "1D"}}},
        "transparency": {"expr": {"Literal": {"Value": "91D"}}},
    }}]
    # Shape visuals also retain an older nested shadow definition. Soften that
    # as well; otherwise the filter tray can still cast the original heavy shadow.
    nested = data.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    nested["dropShadow"] = [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "shadowSpread": {"expr": {"Literal": {"Value": "0D"}}},
        "shadowBlur": {"expr": {"Literal": {"Value": "3D"}}},
        "shadowDistance": {"expr": {"Literal": {"Value": "1D"}}},
        "transparency": {"expr": {"Literal": {"Value": "91D"}}},
    }}]
    write(path, data)


def set_slicer(page, visual_id, x, y, width, height, dropdown=False):
    set_position(page, visual_id, x, y, width, height)
    path = visual_path(page, visual_id)
    data = read(path)
    objects = data.get("visual", {}).get("objects", {})
    # Categorical slicers collapse into compact dropdowns; keep the year
    # slicer in its existing Between mode so its range slider remains usable.
    if dropdown:
        for entry in objects.setdefault("data", [{"properties": {}}]):
            entry.setdefault("properties", {})["mode"] = {
                "expr": {"Literal": {"Value": "'Dropdown'"}}
            }
        for group, size in (("header", "18D"), ("items", "14D")):
            for entry in objects.get(group, []):
                props = entry.setdefault("properties", {})
                if "textSize" in props:
                    props["textSize"] = {"expr": {"Literal": {"Value": size}}}
                if "fontSize" in props:
                    props["fontSize"] = {"expr": {"Literal": {"Value": size}}}
    # Keep the slicer itself flat; the rounded filter tray provides sufficient
    # separation without a second, competing shadow.
    vc = data.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    vc["dropShadow"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
    write(path, data)


def set_card(page, visual_id, x, y, width, height):
    set_position(page, visual_id, x, y, width, height)
    path = visual_path(page, visual_id)
    data = read(path)
    visual = data.setdefault("visual", {})
    objects = visual.setdefault("objects", {})
    # Use the classic single-value Card consistently across KPI visuals. The
    # report currently mixes classic Cards (the reference pair) and new Cards;
    # the new visual applies its own cell padding/background differently, so
    # matching the outer shape alone leaves visibly different tile sizes.
    # These KPI visuals contain only one measure and no reference labels, so
    # migrate the query well and callout formatting without changing the data.
    if visual.get("visualType") == "cardVisual":
        query_state = visual.setdefault("query", {}).setdefault("queryState", {})
        if "Data" in query_state:
            query_state["Values"] = query_state.pop("Data")
        values = objects.pop("value", [])
        objects.pop("label", None)
        objects.pop("layout", None)
        objects.pop("shapeCustomRectangle", None)
        legacy_labels = []
        for item in values:
            legacy_labels.append({"properties": item.get("properties", {})})
        if legacy_labels:
            objects["labels"] = legacy_labels
        visual["visualType"] = "card"
    # Legacy growth reference labels are fixed against 2011, so remove them from
    # the filter-responsive KPI cards rather than implying they recalculate.
    for name in ("referenceLabel", "referenceLabelTitle", "referenceLabelValue", "referenceLabelDetail"):
        objects.pop(name, None)
    for group in ("value", "label"):
        for item in objects.get(group, []):
            props = item.get("properties", {})
            if "fontFamily" in props:
                props["fontFamily"] = {"expr": {"Literal": {"Value": "'''Segoe UI'''"}}}
            if group == "value" and "fontSize" in props:
                props["fontSize"] = {"expr": {"Literal": {"Value": "42D"}}}
                props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{KPI_VALUE}'"}}}}}
            if group == "label" and "fontSize" in props:
                props["fontSize"] = {"expr": {"Literal": {"Value": "15D"}}}
                props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": "'#526174'"}}}}}
    # Legacy Card visuals store their callout formatting in `labels`, unlike
    # the new Card visual which uses `value` and `label`.
    if data.get("visual", {}).get("visualType") == "card":
        for item in objects.get("labels", []):
            props = item.setdefault("properties", {})
            props["fontFamily"] = {"expr": {"Literal": {"Value": "'''Segoe UI'''"}}}
            props["fontSize"] = {"expr": {"Literal": {"Value": "38D"}}}
            props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{KPI_VALUE}'"}}}}}
            props["labelDisplayUnits"] = {"expr": {"Literal": {"Value": "1D"}}}
        # Make the descriptor beneath each callout readable at report scale,
        # while keeping it visually subordinate to the numeric KPI.
        objects["categoryLabels"] = [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "fontFamily": {"expr": {"Literal": {"Value": "'''Segoe UI'''"}}},
            "fontSize": {"expr": {"Literal": {"Value": "16D"}}},
            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{NAVY}'"}}}}},
            "bold": {"expr": {"Literal": {"Value": "true"}}},
        }}]
    # Card (new) uses the `value` group; card (legacy) uses `labels`.
    for group in ("value", "labels"):
        for item in objects.get(group, []):
            item.setdefault("properties", {})["labelDisplayUnits"] = {
                "expr": {"Literal": {"Value": "1D"}}
            }
    # Let the rounded backing shape show through; otherwise the card visual's
    # default white rectangle masks the elevation, making the KPI look inset.
    # visualContainerObjects belongs at the visual JSON root. Keeping it under
    # `visual` is ignored by Power BI; legacy cards then hid the rounded shapes
    # behind their square white fills, which caused mixed corner treatments.
    vc = data.setdefault("visualContainerObjects", {})
    vc["background"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
    vc["border"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
    write(path, data)


def panel(page, bg_id, title_id, title_x=315):
    set_position(page, bg_id, 300, 130, 2200, 145)
    tidy_shape(page, bg_id)
    if title_id:
        set_position(page, title_id, title_x, 142, 145, 40)
        path = visual_path(page, title_id)
        data = read(path)
        for p in data.get("visual", {}).get("objects", {}).get("general", [{}])[0].get("properties", {}).get("paragraphs", []):
            for run in p.get("textRuns", []):
                run["textStyle"].update({"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": NAVY})
        write(path, data)


def set_bg_shape(page, visual_id, x, y, width, height, color=KPI_SURFACE):
    set_position(page, visual_id, x, y, width, height)
    set_shape_fill(page, visual_id, color)
    tidy_shape(page, visual_id)
    path = visual_path(page, visual_id)
    data = read(path)
    border = data["visualContainerObjects"]["border"][0]["properties"]
    border["radius"] = {"expr": {"Literal": {"Value": "18D"}}}
    border["width"] = {"expr": {"Literal": {"Value": "1D"}}}
    border["color"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{KPI_BORDER}'"}}}}}
    shadow = data["visualContainerObjects"]["dropShadow"][0]["properties"]
    shadow["shadowSpread"] = {"expr": {"Literal": {"Value": "0D"}}}
    shadow["shadowBlur"] = {"expr": {"Literal": {"Value": "4D"}}}
    shadow["shadowDistance"] = {"expr": {"Literal": {"Value": "1D"}}}
    shadow["transparency"] = {"expr": {"Literal": {"Value": "88D"}}}
    write(path, data)


def soften_kpi_shadows():
    # KPI cards get only a light lift: preserve the established rounded border
    # while reducing the blur, offset, and opacity of their backing shapes.
    backing_shapes = [
        (OVERVIEW, vid) for vid in (
            "6a8479281b4b1312ee6e", "bcc0f9afa0ec6bb68ffb",
            "9ccabeb5cad809f0102c", "8641d269794d6cd7f40b",
        )
    ] + [
        (TREND, vid) for vid in (
            "cce3182760b09017e6f8", "5964041ac6d460583305",
            "851f4f11badf1f785f60", "f7e66494529135e78379",
            "6411a6a96e41f02af6b8",
        )
    ] + [
        (FORECAST, vid) for vid in (
            "936f8f3c15cf677d2512", "348382caea74e8a9ce53",
            "327290eb154f3d5168eb",
        )
    ]
    for page, visual_id in backing_shapes:
        path = visual_path(page, visual_id)
        data = read(path)
        shadow = {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "shadowSpread": {"expr": {"Literal": {"Value": "0D"}}},
            "shadowBlur": {"expr": {"Literal": {"Value": "4D"}}},
            "shadowDistance": {"expr": {"Literal": {"Value": "1D"}}},
            "transparency": {"expr": {"Literal": {"Value": "88D"}}},
        }
        data.setdefault("visualContainerObjects", {})["dropShadow"] = [{"properties": shadow}]
        data.setdefault("visual", {}).setdefault("visualContainerObjects", {})["dropShadow"] = [{"properties": shadow}]
        write(path, data)


def apply_layouts():
    # The same visual shell is used throughout: a 280 px navigation rail,
    # 120 px title band, a compact filter row, and aligned content cards.
    # Overview
    set_nav(OVERVIEW, "0efd73253f82db9c9e16", "d9f4b77a94d7f3e9ace8", "13e0e7bf8f1dc36e4dd8")
    set_position(OVERVIEW, "47a66917973a99e84ea5", 0, 0, 2560, 120)
    set_shape_fill(OVERVIEW, "47a66917973a99e84ea5", NAVY)
    set_textbox(OVERVIEW, "160616b075e9bb9f632b", x=300, y=8, width=2200, height=106)
    style_overview_header()
    set_position(OVERVIEW, "6bfc209906365236f7a7", 300, 130, 2200, 145)
    tidy_shape(OVERVIEW, "6bfc209906365236f7a7")
    set_textbox(OVERVIEW, "833d4acc5afb9034869e", "BỘ LỌC", 18, 315, 145, 115, 45)
    set_slicer(OVERVIEW, "5c5dc0c13d5a37607189", 445, 150, 610, 100)
    set_slicer(OVERVIEW, "cc44bc0d84e6ef6d3bcd", 1070, 150, 620, 100, dropdown=True)
    set_slicer(OVERVIEW, "26688ebfe2274a4acf06", 1705, 150, 770, 100, dropdown=True)
    kpis = [
        ("51f99c2fcdcfe88497ff", 310), ("0ae5f575996ffbf100e7", 865),
        ("db1a73ede625e4d5e5c8", 1420), ("59dd1f8716609a721f19", 1975),
    ]
    for vid, x in kpis:
        set_card(OVERVIEW, vid, x + 8, 300, 504, 155)
    for sid, x in [("6a8479281b4b1312ee6e", 310), ("bcc0f9afa0ec6bb68ffb", 865),
                   ("9ccabeb5cad809f0102c", 1420), ("8641d269794d6cd7f40b", 1975)]:
        set_bg_shape(OVERVIEW, sid, x, 290, 520, 175)
    set_position(OVERVIEW, "c70c41c1ec644445a7e3", 310, 495, 800, 380)
    set_position(OVERVIEW, "f72c5f97be2b374e88e2", 1135, 495, 1365, 380)
    # Bottom row: give the five-bin release-period chart the wider 60% lane;
    # keep the compact type-by-rating matrix in a 40% lane. Both align to the
    # same outer margins and row height for a deliberate dashboard grid.
    set_position(OVERVIEW, "16f2788db13495de4f6a", 310, 900, 1320, 445)
    set_position(OVERVIEW, "d9e21d82e5f770b95102", 1655, 900, 845, 445)

    # Trend page
    set_nav(TREND, "47ec5c8a4d8678751603", "ad1590ac1a5e7af3ef47", "164629516aaecc7d4013")
    set_position(TREND, "65e89ea34f702f11f2b3", 0, 0, 2560, 120)
    set_shape_fill(TREND, "65e89ea34f702f11f2b3", NAVY)
    set_textbox(TREND, "b89158dff181940788b8", "Xu hướng bổ sung nội dung theo thời gian", 38, 300, 4, 2200, 112)
    panel(TREND, "8002f4ed06b63f6282d8", "c066a11e147313d9aecf")
    set_slicer(TREND, "b8631ed46904bb94d322", 465, 150, 620, 105)
    set_slicer(TREND, "b41ed89b6f612ed14e5e", 1090, 150, 650, 105, dropdown=True)
    set_slicer(TREND, "5c3d17b057aedc9c6ab7", 1745, 150, 730, 105, dropdown=True)
    set_position(TREND, "c066a11e147313d9aecf", 315, 142, 135, 45)
    # Five compact KPIs
    trend_cards = [("72adbc79c4264f26b859", 305), ("d9167e75aee043a54147", 745),
                   ("5ecb102d0e010ac0d29b", 1185), ("c626304cd69fae75ae72", 1625),
                   ("b02c527366c33951d7f5", 2065)]
    trend_shapes = [("cce3182760b09017e6f8", 305), ("5964041ac6d460583305", 745),
                    ("851f4f11badf1f785f60", 1185), ("f7e66494529135e78379", 1625),
                    ("6411a6a96e41f02af6b8", 2065)]
    for vid, x in trend_cards:
        set_card(TREND, vid, x + 6, 300, 388, 145)
    for vid, x in trend_shapes:
        set_bg_shape(TREND, vid, x, 290, 400, 165)
    set_position(TREND, "5e3ca2b9b055ba080a7c", 305, 490, 1050, 405)
    set_position(TREND, "145fcdfd633a7d51e188", 1380, 490, 1120, 405)
    set_position(TREND, "85907bdce5bcd53f7d85", 305, 920, 2195, 425)

    # Country distribution
    set_nav(COUNTRY, "705d7b3293b65847b0c0", "5dd5c9c2934b1e8231bf", "4c3903bbb460be56e947")
    set_position(COUNTRY, "cafafcb5fde98d8c1d6a", 0, 0, 2560, 120)
    set_shape_fill(COUNTRY, "cafafcb5fde98d8c1d6a", NAVY)
    set_textbox(COUNTRY, "6b871c94efabdd00345d", "Phân bố nội dung theo quốc gia", 38, 300, 4, 2200, 112)
    panel(COUNTRY, "fec8de78569f01fca098", "51edd742029e7f39a08e")
    set_slicer(COUNTRY, "67ec019cfda8df81bc51", 465, 150, 620, 105)
    set_slicer(COUNTRY, "eb86b310cac2580de92b", 1090, 150, 650, 105, dropdown=True)
    set_slicer(COUNTRY, "3b1c817990d7711c0873", 1745, 150, 730, 105, dropdown=True)
    set_position(COUNTRY, "51edd742029e7f39a08e", 315, 142, 135, 45)
    # Pair the map with the country ranking for direct geographic comparison;
    # give the Movie/TV composition chart the full lower row for legibility.
    set_position(COUNTRY, "280ce8dd69a2144542df", 305, 310, 1300, 570)
    set_position(COUNTRY, "8fc0ccd709801d96491a", 1630, 310, 870, 570)
    set_position(COUNTRY, "51218840428ca8e6efb3", 305, 915, 2195, 430)

    # Content characteristics
    set_nav(DETAIL, "ea4a7b47ae0662c59f9b", "932f80a93d95a05b7b2d", "344e6aa9711c5dbd6e42")
    set_position(DETAIL, "6fd496e3abc64343402f", 0, 0, 2560, 120)
    set_shape_fill(DETAIL, "6fd496e3abc64343402f", NAVY)
    set_textbox(DETAIL, "5b50344df959ed7748e8", "Đặc điểm nội dung Netflix", 38, 300, 4, 2200, 112)
    panel(DETAIL, "703f8970139cc635dda2", "991448ed186678799efc")
    set_slicer(DETAIL, "499a023a61d7ebdeac4f", 465, 150, 620, 105)
    set_slicer(DETAIL, "82d3c02a2f7584feb021", 1090, 150, 650, 105, dropdown=True)
    set_slicer(DETAIL, "0bebbd2481feec76dfe7", 1745, 150, 730, 105, dropdown=True)
    set_position(DETAIL, "991448ed186678799efc", 315, 142, 135, 45)
    set_position(DETAIL, "0556cf53007cf5a5e56e", 305, 310, 1075, 480)
    set_position(DETAIL, "e17a4a24d426c67ca668", 1410, 310, 1090, 480)
    set_position(DETAIL, "8d8936660ff9a7ecd586", 305, 825, 1075, 520)
    set_position(DETAIL, "15da8eb2e53d980657c5", 1410, 825, 1090, 520)

    # Forecast evaluation: controls/metrics above two aligned chart rows.
    set_nav(FORECAST, "4f8ea93c97a26caa554a", "336b2a7f2e917f41208a", "5fbebc5cb8012e24e52f")
    set_position(FORECAST, "70f0bb8d93a3d64ee4a7", 0, 0, 2560, 120)
    set_shape_fill(FORECAST, "70f0bb8d93a3d64ee4a7", NAVY)
    set_textbox(FORECAST, "5e0a18d4ff923c4c2396", "Đánh giá mô hình dự báo", 38, 300, 4, 2200, 112)
    for vid, x in [("10224178acc58897c3d0", 330), ("4c9491c3393249a032c3", 750), ("5e4cbcd549dbdd38459f", 1170)]:
        set_card(FORECAST, vid, x + 5, 160, 360, 145)
    set_bg_shape(FORECAST, "936f8f3c15cf677d2512", 330, 150, 370, 165)
    set_bg_shape(FORECAST, "348382caea74e8a9ce53", 750, 150, 370, 165)
    set_bg_shape(FORECAST, "327290eb154f3d5168eb", 1170, 150, 370, 165)
    set_bg_shape(FORECAST, "d69c378bca49ec77fb9e", 1770, 150, 480, 165)
    set_slicer(FORECAST, "5eb847f7ef34986068a4", 1790, 165, 440, 130)
    set_position(FORECAST, "3df8bd8a669a99a55266", 305, 350, 1075, 455)
    set_position(FORECAST, "77bb4f12365312e52c16", 1410, 350, 1090, 455)
    set_position(FORECAST, "511138d6f6140dfc0de6", 305, 835, 1075, 510)
    set_position(FORECAST, "6d4abbedbf1896b33975", 1410, 835, 1090, 510)


def apply_theme():
    theme_path = REPORT / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU09.json"
    theme = read(theme_path)
    # Aquatic palette inspired by the reference: petrol blue anchors the
    # dashboard, turquoise distinguishes the secondary series, and pale
    # blue-green tones support categorical visuals without introducing red.
    theme["dataColors"] = [MOVIE_BLUE, SHOW_TEAL, "#3C9A9B", "#8ACBC0", "#4F9FB0", "#79B7C1", "#B5DDD6", "#2E6874"]
    theme.update({
        "foreground": TEXT,
        "foregroundNeutralSecondary": "#52727A",
        "foregroundNeutralTertiary": "#77949A",
        "foregroundNeutralLight": "#D2E8E4",
        "background": "#FFFFFF",
        "backgroundLight": OFF_WHITE,
        "backgroundNeutral": "#DCEFEB",
        "backgroundDark": "#C6E3DE",
        "tableAccent": MOVIE_BLUE,
        "shapeStroke": "#C5E0DB",
        "disabledText": "#819B9F",
        "good": SHOW_TEAL,
        "neutral": "#A1C9C1",
        "bad": "#809CA0",
        "maximum": NAVY,
        "center": SHOW_TEAL,
        "minimum": "#E6F3F0",
    })
    card_style = theme.setdefault("visualStyles", {}).setdefault("cardVisual", {}).setdefault("*", {})
    card_style["value"] = [{"$id": "default", "labelDisplayUnits": 1}]
    card_style["shapeCustomRectangle"] = [{
        "$id": "default", "tileShape": "rectangleRounded", "rectangleRoundedCurve": 18,
    }]
    card_style["layout"] = [{"$id": "default", "backgroundShow": False}]
    card_style["*"] = [{"$id": "default", "backgroundTransparency": 100}]
    nav_style = theme.setdefault("visualStyles", {}).setdefault("pageNavigator", {}).setdefault("*", {})
    selected_fill = next((item for item in nav_style.setdefault("fill", []) if item.get("$id") == "selected"), None)
    if selected_fill is not None:
        selected_fill["fillColor"] = {"solid": {"color": NAV_SELECTED}}
    selected_text = next((item for item in nav_style.setdefault("text", []) if item.get("$id") == "selected"), None)
    if selected_text is not None:
        selected_text["fontColor"] = {"solid": {"color": NAVY}}
        selected_text["fontWeight"] = "bold"
    for cls in theme.get("textClasses", {}).values():
        if isinstance(cls, dict):
            cls["fontFace"] = "Segoe UI"
            cls["color"] = TEXT
    write(theme_path, theme)

    # Keep the registered BaseTheme identity and path unchanged; only palette
    # and semantic colors change, avoiding a broken resource-package reference.


def normalize_visual_fonts():
    for file in PAGES.glob("*/visuals/*/visual.json"):
        data = read(file)
        vis = data.get("visual", {})
        objects = vis.get("objects", {})
        # Replace hard-coded legacy serif labels with the same UI family as the theme.
        serialized = json.dumps(objects, ensure_ascii=False)
        serialized = serialized.replace("Times New Roman", "Segoe UI")
        vis["objects"] = json.loads(serialized)
        # Chart titles live under visualContainerObjects, not `objects`.
        container_objects = vis.setdefault("visualContainerObjects", {})
        for title in container_objects.get("title", []):
            props = title.setdefault("properties", {})
            props["fontFamily"] = {"expr": {"Literal": {"Value": "'''Segoe UI'''"}}}
            props["fontSize"] = {"expr": {"Literal": {"Value": "20D"}}}
            props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{NAVY}'"}}}}}
            props["bold"] = {"expr": {"Literal": {"Value": "true"}}}
            # Separate chart headings from the plotting area with a quiet,
            # consistent pale-blue title band and a slim teal divider.
            props["background"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{TITLE_BAND}'"}}}}}
            props["alignment"] = {"expr": {"Literal": {"Value": "'left'"}}}
            props["titleWrap"] = {"expr": {"Literal": {"Value": "true"}}}
        if container_objects.get("title"):
            container_objects["divider"] = [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{TITLE_DIVIDER}'"}}}}},
                "width": {"expr": {"Literal": {"Value": "1D"}}},
            }}]
        # Expand abbreviated K labels to full numeric values on chart axes.
        if vis.get("visualType") in {
            "barChart", "clusteredBarChart", "columnChart", "clusteredColumnChart",
            "stackedColumnChart", "lineChart", "areaChart", "stackedAreaChart",
            "scatterChart", "comboChart",
        }:
            axis = vis.setdefault("objects", {}).setdefault("valueAxis", [{}])
            if not axis:
                axis.append({})
            for entry in axis:
                entry.setdefault("properties", {})["labelDisplayUnits"] = {
                    "expr": {"Literal": {"Value": "1D"}}
                }
        # Power BI uses 0D/Auto on some pie/donut data labels and card callouts.
        # Force every existing display-unit property to 1D/None across every
        # visual, including visuals that do not have a conventional value axis.
        def full_units(node):
            if isinstance(node, dict):
                for key in ("labelDisplayUnits", "displayUnits"):
                    if key in node:
                        node[key] = {"expr": {"Literal": {"Value": "1D"}}}
                for value in node.values():
                    full_units(value)
            elif isinstance(node, list):
                for value in node:
                    full_units(value)
        full_units(vis.get("objects", {}))
        write(file, data)


def soften_analytical_visual_shadows():
    # Keep a subtle edge beneath charts/tables/maps without the heavy gray halo
    # that was making neighboring visuals compete for attention. KPI tiles and
    # navigation elements are intentionally left alone.
    analytical_types = {
        "barChart", "clusteredBarChart", "columnChart", "clusteredColumnChart",
        "stackedColumnChart", "lineChart", "areaChart", "stackedAreaChart",
        "scatterChart", "comboChart", "pieChart", "donutChart", "treemap",
        "pivotTable", "map",
    }
    for file in PAGES.glob("*/visuals/*/visual.json"):
        data = read(file)
        visual = data.get("visual", {})
        if visual.get("visualType") not in analytical_types:
            continue
        shadows = visual.setdefault("visualContainerObjects", {}).get("dropShadow", [])
        for shadow in shadows:
            props = shadow.setdefault("properties", {})
            props["show"] = {"expr": {"Literal": {"Value": "true"}}}
            props["shadowSpread"] = {"expr": {"Literal": {"Value": "1D"}}}
            props["shadowBlur"] = {"expr": {"Literal": {"Value": "4D"}}}
            props["shadowDistance"] = {"expr": {"Literal": {"Value": "2D"}}}
            props["transparency"] = {"expr": {"Literal": {"Value": "82D"}}}
        write(file, data)


def enable_bar_value_labels():
    # Put exact values on bars where the number of categories is small enough
    # to remain readable. Dense country-by-country and duration histograms keep
    # their tooltips to avoid overlapping labels.
    chart_ids = [
        (OVERVIEW, "f72c5f97be2b374e88e2"),  # rating by Movie / TV Show
        (OVERVIEW, "16f2788db13495de4f6a"),  # release-period totals
        (TREND, "85907bdce5bcd53f7d85"),     # annual additions by type
        (DETAIL, "0556cf53007cf5a5e56e"),    # TV Show seasons
        (COUNTRY, "8fc0ccd709801d96491a"),  # top countries
        (FORECAST, "511138d6f6140dfc0de6"),  # forecast residuals
    ]
    for page, visual_id in chart_ids:
        path = visual_path(page, visual_id)
        data = read(path)
        labels = data.setdefault("visual", {}).setdefault("objects", {}).setdefault("labels", [])
        if not labels:
            labels.append({"properties": {}})
        props = labels[0].setdefault("properties", {})
        props["show"] = {"expr": {"Literal": {"Value": "true"}}}
        props["fontSize"] = {"expr": {"Literal": {"Value": "16D"}}}
        props["labelDisplayUnits"] = {"expr": {"Literal": {"Value": "1D"}}}
        props["labelOverflow"] = {"expr": {"Literal": {"Value": "true"}}}
        write(path, data)
    # The rating comparison has paired series and the most compact labels in
    # the overview; enlarge only this visual further so the exact counts read
    # clearly without inflating labels across denser charts.
    path = visual_path(OVERVIEW, "f72c5f97be2b374e88e2")
    data = read(path)
    data["visual"]["objects"]["labels"][0]["properties"]["fontSize"] = {
        "expr": {"Literal": {"Value": "48D"}}
    }
    data["visual"]["objects"]["labels"][0]["properties"]["bold"] = {
        "expr": {"Literal": {"Value": "true"}}
    }
    write(path, data)


def color_fill(color):
    return {"solid": {"color": {"expr": {"Literal": {"Value": f"'{color}'"}}}}}


def set_visual_colors(page, visual_id, color):
    path = visual_path(page, visual_id)
    data = read(path)
    objects = data.setdefault("visual", {}).setdefault("objects", {})
    objects["dataPoint"] = [{
        "properties": {"fill": color_fill(color)},
        "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]},
    }]
    write(path, data)


def add_category_colors(page, visual_id, entity, field, mapping):
    path = visual_path(page, visual_id)
    data = read(path)
    objects = data.setdefault("visual", {}).setdefault("objects", {})
    entries = []
    for category, color in mapping.items():
        entries.append({
            "properties": {"fill": color_fill(color)},
            "selector": {"data": [{"scopeId": {"Comparison": {
                "ComparisonKind": 0,
                "Left": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": field}},
                "Right": {"Literal": {"Value": f"'{category}'"}},
            }}}]},
        })
    objects["dataPoint"] = entries
    write(path, data)


def recolor_type_series(page, visual_id, colors):
    # Clone the known-good Series conditional format from the country chart,
    # then change only the Movie/TV Show colors.
    import copy
    source = read(visual_path(COUNTRY, "51218840428ca8e6efb3"))
    template = source["visual"]["objects"]["dataPoint"][0]
    entry = copy.deepcopy(template)
    cases = entry["properties"]["fill"]["solid"]["color"]["expr"]["Conditional"]["Cases"]
    for case in cases:
        category = case["Condition"]["Comparison"]["Right"]["Literal"]["Value"].strip("'")
        if category in colors:
            case["Value"]["Literal"]["Value"] = f"'{colors[category]}'"
    data = read(visual_path(page, visual_id))
    objects = data.setdefault("visual", {}).setdefault("objects", {})
    objects["dataPoint"] = [entry, {"properties": {"fillTransparency": {"expr": {"Literal": {"Value": "0D"}}}}}]
    write(visual_path(page, visual_id), data)


def set_line_colors(page, visual_id, mapping):
    path = visual_path(page, visual_id)
    data = read(path)
    entries = []
    for query_ref, color in mapping.items():
        entries.append({
            "properties": {"strokeColor": color_fill(color)},
            "selector": {"metadata": query_ref},
        })
    data.setdefault("visual", {}).setdefault("objects", {})["lineStyles"] = entries
    write(path, data)


def recolor_literals(page, visual_id, mapping):
    path = visual_path(page, visual_id)
    data = read(path)
    serialized = json.dumps(data, ensure_ascii=False)
    for old, new in mapping.items():
        serialized = serialized.replace(old, new)
    write(path, json.loads(serialized))


def set_gradient(page, visual_id, minimum, maximum):
    """Set a visual's conditional-format scale directly, independent of old theme literals."""
    path = visual_path(page, visual_id)
    data = read(path)
    serialized = json.dumps(data, ensure_ascii=False)
    # Each affected matrix/treemap stores its scale inside a FillRule node;
    # update only the min/max endpoints, preserving its measure and null policy.
    def update(node):
        if isinstance(node, dict):
            gradient = node.get("linearGradient2")
            if isinstance(gradient, dict):
                for key, color in (("min", minimum), ("max", maximum)):
                    if key in gradient and "color" in gradient[key]:
                        gradient[key]["color"]["Literal"]["Value"] = f"'{color}'"
            for value in node.values():
                update(value)
        elif isinstance(node, list):
            for value in node:
                update(value)
    update(data)
    write(path, data)


def apply_chart_palette():
    movie_tv = {"Movie": MOVIE_BLUE, "TV Show": SHOW_TEAL}

    # Give Movie and TV Show the same semantic colors on every comparison.
    add_category_colors(OVERVIEW, "c70c41c1ec644445a7e3", "dim_title", "type", movie_tv)
    recolor_type_series(OVERVIEW, "f72c5f97be2b374e88e2", movie_tv)
    recolor_type_series(TREND, "85907bdce5bcd53f7d85", movie_tv)
    recolor_type_series(COUNTRY, "51218840428ca8e6efb3", movie_tv)

    # Single-series visuals use calm supporting colors; heatmaps use the same
    # pale-aqua to deep-water gradient as the dashboard's overall theme.
    set_visual_colors(OVERVIEW, "16f2788db13495de4f6a", MOVIE_BLUE)
    set_visual_colors(DETAIL, "0556cf53007cf5a5e56e", TEAL)
    set_visual_colors(DETAIL, "15da8eb2e53d980657c5", TEAL)
    set_visual_colors(FORECAST, "511138d6f6140dfc0de6", "#4F9FB0")
    set_visual_colors(FORECAST, "6d4abbedbf1896b33975", MOVIE_BLUE)

    # The one-series trend line and geographic map are teal; Top Countries use amber.
    line = read(visual_path(TREND, "145fcdfd633a7d51e188"))
    line_obj = line["visual"]["objects"]["lineStyles"][0]["properties"]["strokeColor"]
    line_obj["solid"]["color"]["expr"]["Literal"]["Value"] = f"'{SHOW_TEAL}'"
    write(visual_path(TREND, "145fcdfd633a7d51e188"), line)
    map_data = read(visual_path(COUNTRY, "280ce8dd69a2144542df"))
    map_data["visual"]["objects"]["dataPoint"][1]["properties"]["fill"] = color_fill(SHOW_TEAL)
    write(visual_path(COUNTRY, "280ce8dd69a2144542df"), map_data)
    # The Top Countries visual has explicit conditional assignments for the
    # highlighted countries; replace its legacy orange directly as well.
    recolor_literals(COUNTRY, "8fc0ccd709801d96491a", {"#E6A23C": AMBER, "#F4E0A5": AMBER})

    # Rating categories stay distinct while following an aquatic blue-green ramp.
    add_category_colors(DETAIL, "e17a4a24d426c67ca668", "dim_title", "Rating Group", {
        "TV-MA": "#126B78", "TV-14": "#167C8A", "Others": "#3C9A9B",
        "TV-PG": "#62B3A8", "R": "#82C5B8", "PG-13": "#4F9FB0",
    })

    # Use quiet, matching pale-aqua-to-deep-water scales for treemaps/matrices.
    set_gradient(TREND, "5e3ca2b9b055ba080a7c", "#E4F3F0", "#167C8A")
    set_gradient(OVERVIEW, "d9e21d82e5f770b95102", "#EAF6F4", "#3C9A9B")
    set_gradient(DETAIL, "8d8936660ff9a7ecd586", "#E7F4F1", "#4F9F9A")

    # Forecast actual/forecast series get separate, meaningful line colors.
    set_line_colors(FORECAST, "3df8bd8a669a99a55266", {
        "Sum(forecast_vs_actual_2021.actual)": MOVIE_BLUE,
        "CountNonNull(forecast_vs_actual_2021.forecast)": SHOW_TEAL,
    })
    set_line_colors(FORECAST, "77bb4f12365312e52c16", {
        "CountNonNull(forecast_12_months.forecast)": SHOW_TEAL,
        "GROWTH THRESHOLD.Threshold Line": MOVIE_BLUE,
    })

    # Smooth the canvas tone consistently across every report page.
    for page in (OVERVIEW, TREND, COUNTRY, DETAIL, FORECAST):
        path = PAGES / page / "page.json"
        data = read(path)
        bg = data.get("objects", {}).get("background", [])
        if bg:
            color = bg[0]["properties"]["color"]["solid"]["color"]["expr"]
            color.clear()
            color["Literal"] = {"Value": f"'{OFF_WHITE}'"}
        write(path, data)


def apply_chrome_colors():
    # Maintain a consistent hierarchy on every page: deep petrol title band,
    # brighter teal navigation rail, and a quiet pale-aqua canvas.
    title_bars = [
        (OVERVIEW, "47a66917973a99e84ea5"), (TREND, "65e89ea34f702f11f2b3"),
        (COUNTRY, "cafafcb5fde98d8c1d6a"), (DETAIL, "6fd496e3abc64343402f"),
        (FORECAST, "70f0bb8d93a3d64ee4a7"),
    ]
    nav_rails = [
        (OVERVIEW, "13e0e7bf8f1dc36e4dd8"), (TREND, "164629516aaecc7d4013"),
        (COUNTRY, "4c3903bbb460be56e947"), (DETAIL, "344e6aa9711c5dbd6e42"),
        (FORECAST, "5fbebc5cb8012e24e52f"),
    ]
    for page, visual_id in title_bars:
        set_shape_fill(page, visual_id, NAVY)
    for page, visual_id in nav_rails:
        set_shape_fill(page, visual_id, NAVY_DARK)


def main():
    apply_layouts()
    soften_kpi_shadows()
    apply_chrome_colors()
    normalize_visual_fonts()
    enable_bar_value_labels()
    soften_analytical_visual_shadows()
    apply_theme()
    apply_chart_palette()
    # Also set each page canvas to a quiet neutral so white cards read clearly.
    for page in (OVERVIEW, TREND, COUNTRY, DETAIL, FORECAST):
        page_file = PAGES / page / "page.json"
        data = read(page_file)
        # Keep existing display name, canvas dimensions, and page state untouched.
        write(page_file, data)


if __name__ == "__main__":
    main()
