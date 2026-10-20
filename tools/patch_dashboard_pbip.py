from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(r"C:\WorkSpace\DV\project\Project_DataVisualization\dashboard")
MODEL = ROOT / "Dashboard_Custom.SemanticModel" / "definition"
REPORT = ROOT / "Dashboard_Custom.Report" / "definition"
OVERVIEW = REPORT / "pages" / "a1ab8509b3eee61b13ac"
VISUALS = OVERVIEW / "visuals"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def visual(visual_id: str):
    return VISUALS / visual_id / "visual.json"


def set_position(path: Path, *, x: float, y: float, width: float, height: float):
    data = read_json(path)
    data["position"].update({"x": x, "y": y, "width": width, "height": height})
    write_json(path, data)


def replace_in_files(files, replacements):
    for path in files:
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def column_projection(entity: str, prop: str, query_ref: str, native: str):
    return {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": entity}},
                "Property": prop,
            }
        },
        "queryRef": query_ref,
        "nativeQueryRef": native,
        "active": True,
    }


def main():
    dim_title = MODEL / "tables" / "dim_title.tmdl"
    bridge_country = MODEL / "tables" / "bridge_country.tmdl"
    relationships = MODEL / "relationships.tmdl"

    # Make KPI names explicit and filter-aware. The formulas already respect
    # the current filter context; only the misleading 2020-era names are changed.
    replacements = [
        ("Tốc độ tăng trưởng nội dung", "Tổng nội dung theo bộ lọc"),
        ("Tốc độ tăng trưởng movie", "Movie theo bộ lọc"),
        ("Tốc độ tăng trưởng TV Show", "TV Show theo bộ lọc"),
        ("Sự phân bổ nội dung cho các quốc gia", "Số quốc gia có nội dung"),
        ("Titles Added 2020", "Tổng nội dung theo bộ lọc"),
        ("Movies Added 2020", "Movie theo bộ lọc"),
        ("TV Shows Added 2020", "TV Show theo bộ lọc"),
        ("Countries 2020", "Số quốc gia có nội dung"),
    ]
    replace_in_files([dim_title, bridge_country], replacements[:4])

    # Update report metadata/query references for the renamed measures.
    visual_files = list(REPORT.glob("pages/*/visuals/*/visual.json"))
    replace_in_files(
        visual_files,
        replacements[:4]
        + replacements[4:]
        + [
            ("Actual vs Forecast by Month", "Tổng nội dung: Actual vs Forecast theo tháng"),
            ("Forecast vs Growth Threshold", "Tổng nội dung dự báo và ngưỡng tăng trưởng"),
            ("Prediction Error by Month", "Sai số dự báo tổng nội dung theo tháng"),
            ("Actual vs Forecast Relationship", "Quan hệ Actual–Forecast của tổng nội dung"),
            (
                "Lượng nội dung Netflix được dự báo có xu hướng tăng đều trong các tháng tiếp theo, tuy nhiên mô hình Hồi quy tuyến tính chưa phản ánh tốt các biến động thực tế theo từng tháng.",
                "Tổng số nội dung Netflix (Movie + TV Show) được dự báo theo tháng. Mô hình hiện tại dùng biến xu hướng thời gian; cần bổ sung mùa vụ và biến trễ để phản ánh tốt hơn biến động theo tháng.",
            ),
        ],
    )

    # Keep the filter caption compact so it is not clipped in the top filter row.
    filter_caption = visual("833d4acc5afb9034869e")
    caption = read_json(filter_caption)
    run = caption["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
    run["value"] = "BỘ LỌC"
    run["textStyle"]["fontSize"] = "28pt"
    write_json(filter_caption, caption)

    # Allow country slicers/KPIs to propagate through the title bridge.
    rel_text = relationships.read_text(encoding="utf-8")
    needle = (
        "relationship AutoDetected_fb4f2d19-aa57-4e23-8546-42dc57637831\n"
        "\tfromColumn: bridge_country.show_id\n"
        "\ttoColumn: dim_title.show_id"
    )
    replacement = (
        "relationship AutoDetected_fb4f2d19-aa57-4e23-8546-42dc57637831\n"
        "\tcrossFilteringBehavior: bothDirections\n"
        "\tfromColumn: bridge_country.show_id\n"
        "\ttoColumn: dim_title.show_id"
    )
    if needle in rel_text and "crossFilteringBehavior" not in rel_text[rel_text.index(needle):rel_text.index(needle) + len(needle) + 80]:
        rel_text = rel_text.replace(needle, replacement)
        relationships.write_text(rel_text, encoding="utf-8")

    # Overview layout: keep title at the top, place slicers in a dedicated row,
    # then use a regular grid for KPI cards and related visuals.
    set_position(visual("833d4acc5afb9034869e"), x=480, y=145, width=220, height=70)  # filter heading
    set_position(visual("6bfc209906365236f7a7"), x=470, y=135, width=1750, height=215)  # filter container
    set_position(visual("5c5dc0c13d5a37607189"), x=720, y=190, width=430, height=125)  # year
    set_position(visual("cc44bc0d84e6ef6d3bcd"), x=1200, y=190, width=470, height=125)  # rating
    set_position(visual("26688ebfe2274a4acf06"), x=1720, y=190, width=450, height=125)  # type

    card_positions = {
        "51f99c2fcdcfe88497ff": (480, 390, 400, 205),
        "0ae5f575996ffbf100e7": (920, 390, 400, 205),
        "db1a73ede625e4d5e5c8": (1360, 390, 400, 205),
        "59dd1f8716609a721f19": (1800, 390, 400, 205),
    }
    for vid, (x, y, w, h) in card_positions.items():
        set_position(visual(vid), x=x, y=y, width=w, height=h)

    # Move the four card backgrounds with the cards.
    shape_positions = {
        "6a8479281b4b1312ee6e": (470, 375, 420, 230),
        "bcc0f9afa0ec6bb68ffb": (910, 375, 420, 230),
        "9ccabeb5cad809f0102c": (1350, 375, 420, 230),
        "8641d269794d6cd7f40b": (1790, 375, 420, 230),
    }
    for vid, (x, y, w, h) in shape_positions.items():
        set_position(visual(vid), x=x, y=y, width=w, height=h)

    set_position(visual("c70c41c1ec644445a7e3"), x=480, y=650, width=680, height=360)
    set_position(visual("f72c5f97be2b374e88e2"), x=1200, y=650, width=1000, height=360)
    set_position(visual("16f2788db13495de4f6a"), x=480, y=1040, width=800, height=320)
    set_position(visual("d9e21d82e5f770b95102"), x=1320, y=1040, width=880, height=300)

    # Convert the rating visual to clustered columns with Movie/TV Show series.
    rating_path = visual("f72c5f97be2b374e88e2")
    rating = read_json(rating_path)
    rating["visual"]["visualType"] = "clusteredColumnChart"
    qs = rating["visual"]["query"]["queryState"]
    qs["Series"] = {
        "projections": [column_projection("dim_title", "type", "dim_title.type", "type")]
    }
    objects = rating["visual"].setdefault("objects", {})
    objects["categoryAxis"] = [{"properties": {
        "fontSize": {"expr": {"Literal": {"Value": "16D"}}},
        "fontFamily": {"expr": {"Literal": {"Value": "'''Times New Roman'''"}}},
    }}]
    objects["valueAxis"] = [{"properties": {
        "fontSize": {"expr": {"Literal": {"Value": "16D"}}},
        "fontFamily": {"expr": {"Literal": {"Value": "'''Times New Roman'''"}}},
    }}]
    rating["visual"].setdefault("visualContainerObjects", {}).setdefault("title", [{}])[0].setdefault("properties", {})[
        "text"
    ] = {"expr": {"Literal": {"Value": "'Số lượng nội dung theo rating: Movie và TV Show'"}}}
    write_json(rating_path, rating)

    # Improve KPI hierarchy without changing the underlying data.
    for vid in card_positions:
        path = visual(vid)
        data = read_json(path)
        objects = data["visual"].setdefault("objects", {})
        objects["value"] = [{"properties": {
            "fontSize": {"expr": {"Literal": {"Value": "36D"}}},
            "fontFamily": {"expr": {"Literal": {"Value": "'''Times New Roman'''"}}},
            "horizontalAlignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }, "selector": {"id": "default"}}]
        objects["label"] = [{"properties": {
            "fontSize": {"expr": {"Literal": {"Value": "18D"}}},
            "fontFamily": {"expr": {"Literal": {"Value": "'''Times New Roman'''"}}},
            "textWrap": {"expr": {"Literal": {"Value": "true"}}},
        }, "selector": {"id": "default"}}]
        write_json(path, data)

    print("PBIP dashboard patched")


if __name__ == "__main__":
    main()
