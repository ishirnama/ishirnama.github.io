import re
import json
import numpy as np
import pandas as pd
from matplotlib import colormaps

CSV = r"c:\Users\ishir\Desktop\Portfolio\SCOTLAND_SEAS\2022.23_PhD_NA_beachCleanData.csv"
OUT_TOP3 = r"c:\Users\ishir\Desktop\Portfolio\files\scotland_top3_plastics.html"
OUT_SEVERITY = r"c:\Users\ishir\Desktop\Portfolio\files\scotland_severity_map.html"

df = pd.read_csv(CSV)


def top_3_plastics(plastic_row, plastic_names):
    indices = np.argsort(plastic_row)[-3:][::-1]
    return [(plastic_names[i], plastic_row[i]) for i in indices if plastic_row[i] > 0]


def normalise_object(obj):
    # split camelCase into words (e.g. "fragmentMed" -> "fragment Med")
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", obj)
    tokens = re.findall(r"[a-z]+", spaced.lower())
    size_words = {"sml", "med", "lrg", "small", "medium", "large"}
    return [t for t in tokens if t not in size_words]


def _singular(token):
    if token.endswith("ies") and len(token) > 3:
        return token[:-3] + "y"
    if token.endswith("es"):
        return token[:-2]
    if token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def classify_object(tokens):
    categories = set()
    for category, keywords in OBJECT_CATEGORY_RULES.items():
        for t in tokens:
            if t in keywords or _singular(t) in keywords:
                categories.add(category)
    if not categories:
        categories.add("other")
    return list(categories)


def severity_radius(s, scale=25):
    return scale * np.sqrt(s / S.max())


def split_beaches_sampled_twice(df, beach_col="beach", date_col="date"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True)
    df = df.sort_values([beach_col, date_col])
    counts = df[beach_col].value_counts()
    valid_beaches = counts[counts == 2].index
    df_twice = df[df[beach_col].isin(valid_beaches)]
    df_1 = df_twice.groupby(beach_col).nth(0).reset_index()
    df_2 = df_twice.groupby(beach_col).nth(1).reset_index()
    return df_1, df_2


df_1, df_2 = split_beaches_sampled_twice(df)

beaches = list(df_1["beach"])
coords = df_1.iloc[:, 6:8].to_numpy()
plastics_1, plastics_2 = df_1.iloc[:, 37:168], df_2.iloc[:, 37:168]
plastic_types = list(plastics_1.columns)
avg_plastics = 0.5 * (plastics_1.to_numpy() + plastics_2.to_numpy())

split_by_dots = lambda s: ["_".join(v.split("..")) if ".." in v else v for v in s]
split_by_dash = lambda s: [v.split("_") if "_" in v else v for v in s]
plastic_names = np.array(split_by_dash(split_by_dots(plastic_types)))

OBJECT_CATEGORY_RULES = {
    "fishing_gear": {"fishingnet", "fishline", "lobster", "crab", "pot", "buoy", "oyster", "hook"},
    "microplastics": {"fragment", "nurdle", "pellet", "foam"},
    "consumer_packaging": {"bag", "bottle", "cup", "wrapper", "container", "packaging"},
    "hazardous": {"oil", "fertiliser", "cartridge", "shotgun", "paraffin"},
    "personal_items": {"cigarette", "lighter", "pen", "shoe", "toy", "comb", "sunglasses", "glove"},
    "industrial": {"crate", "jerry", "hardhat", "strapping", "fibreglass", "drum"},
    "sanitary_medical": {"condom", "tampon", "wipe", "syringe", "facemask"},
}

CATEGORY_SEVERITY = {
    "microplastics": 4.0,
    "fishing_gear": 3.5,
    "hazardous": 4.5,
    "sanitary_medical": 3.0,
    "industrial": 2.5,
    "consumer_packaging": 2.0,
    "personal_items": 1.5,
    "other": 1.0,
}

MATERIAL_MULTIPLIER = {
    "plastic": 1.0,
    "polystyrene": 1.2,
    "rubber": 1.1,
    "metal": 0.8,
    "glass": 0.6,
    "wood": 0.5,
    "cloth": 0.7,
    "paper": 0.6,
    "sanitary": 1.3,
    "medical": 1.4,
    "pollutants": 2.0,
}

plastic_metadata = []
for row in plastic_names:
    survey, material, obj = row
    tokens = normalise_object(obj)
    categories = classify_object(tokens)
    plastic_metadata.append(
        {"material": material, "object": obj, "tokens": tokens, "categories": categories}
    )

W = []
for meta in plastic_metadata:
    cat_score = np.mean([CATEGORY_SEVERITY[c] for c in meta["categories"]])
    mat_mult = MATERIAL_MULTIPLIER.get(meta["material"], 1.0)
    W.append(cat_score * mat_mult)
W = np.array(W)
W = W / W.sum()

N = avg_plastics.shape[0]
S = (W @ avg_plastics.T) / N

# ---- Build data for the two maps ----
top3_data = []
for i in range(len(beaches)):
    top3 = top_3_plastics(avg_plastics[i], plastic_types)
    top3_data.append(
        {
            "lat": float(coords[i][0]),
            "lon": float(coords[i][1]),
            "name": beaches[i],
            "items": [[n, round(float(v), 2)] for n, v in top3],
        }
    )

cmap = colormaps["viridis"]
smin, smax = float(S.min()), float(S.max())
severity_data = []
for i in range(len(beaches)):
    s = float(S[i])
    t = (s - smin) / (smax - smin) if smax > smin else 0.0
    r, g, b, _ = cmap(t)
    color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
    severity_data.append(
        {
            "lat": float(coords[i][0]),
            "lon": float(coords[i][1]),
            "name": beaches[i],
            "s": round(s, 3),
            "color": color,
            "radius": round(float(severity_radius(s)), 2),
        }
    )


# ---- HTML templates ----

def leaflet_html(title, tiles, attribution, extra_css, init_js, body_extra=""):
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{title}</title>\n"
        "<link rel=\"stylesheet\" href=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.css\">\n"
        "<script src=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.js\"></script>\n"
        "<style>\n"
        "html, body { height: 100%; margin: 0; }\n"
        "#map { height: 100%; width: 100%; }\n"
        ".legend { background: rgba(255,255,255,0.92); padding: 10px 12px; "
        "border-radius: 6px; box-shadow: 0 1px 5px rgba(0,0,0,.3); "
        "font: 12px/1.6 Helvetica, Arial, sans-serif; color: #222; }\n"
        ".legend .bar { width: 150px; height: 10px; border-radius: 2px; }\n"
        ".legend .labels { display: flex; justify-content: space-between; margin-top: 3px; }\n"
        + extra_css +
        "</style>\n</head>\n<body>\n"
        f"<div id=\"map\"></div>\n{body_extra}\n"
        "<script>\n"
        f"var map = L.map('map').setView([56.5, -4.0], 6);\n"
        f"L.tileLayer('{tiles}', {{ maxZoom: 19, attribution: '{attribution}' }}).addTo(map);\n"
        + init_js +
        "</script>\n</body>\n</html>\n"
    )


# --- Map 1: top-3 plastics (markers) ---
top3_js = (
    "var data = " + json.dumps(top3_data) + ";\n"
    "data.forEach(function(d){\n"
    "  var lines = d.items.map(function(it){ return it[0] + ': ' + it[1]; }).join('<br>');\n"
    "  var html = '<b>' + d.name + '</b><br>' + (lines || 'No plastics recorded');\n"
    "  L.marker([d.lat, d.lon]).addTo(map).bindPopup(html, { maxWidth: 260 });\n"
    "});\n"
)
top3_legend = (
    "<div class=\"legend\" style=\"position:absolute; bottom:20px; left:12px; z-index:1000;\">"
    "<b>Top 3 plastics per beach</b><br>Click a marker to inspect.</div>"
)
with open(OUT_TOP3, "w", encoding="utf-8") as f:
    f.write(
        leaflet_html(
            "Top 3 plastics per Scottish beach",
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            "&copy; OpenStreetMap contributors",
            "",
            top3_js,
            top3_legend,
        )
    )

# --- Map 2: severity heatmap (circles + legend) ---
stops = [cmap(i / 9) for i in range(10)]
grad = "linear-gradient(to right, " + ", ".join(
    "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
    for r, g, b, _ in stops
) + ")"

sev_js = (
    "var data = " + json.dumps(severity_data) + ";\n"
    "data.forEach(function(d){\n"
    "  L.circleMarker([d.lat, d.lon], {\n"
    "    radius: d.radius, color: d.color, fillColor: d.color, fillOpacity: 0.75, weight: 1\n"
    "  }).addTo(map)\n"
    "    .bindPopup('<b>' + d.name + '</b><br><b>Severity score:</b> ' + d.s, { maxWidth: 250 })\n"
    "    .bindTooltip(d.name + ' | ' + d.s);\n"
    "});\n"
)
sev_legend = (
    "<div class=\"legend\" style=\"position:absolute; bottom:20px; left:12px; z-index:1000;\">"
    "<b>Pollution severity score</b><br>"
    f"<div class=\"bar\" style=\"background:{grad};\"></div>"
    f"<div class=\"labels\"><span>lower ({smin:.3f})</span><span>higher ({smax:.3f})</span></div>"
    "<div style=\"margin-top:4px;\">Circle size &amp; colour scale with score.</div></div>"
)
with open(OUT_SEVERITY, "w", encoding="utf-8") as f:
    f.write(
        leaflet_html(
            "Plastic pollution severity on Scottish beaches",
            "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            "&copy; OpenStreetMap contributors &copy; CARTO",
            "",
            sev_js,
            sev_legend,
        )
    )

# ---- Summary stats for the write-up ----
order = np.argsort(S)[::-1]
print("Number of beaches sampled twice (N):", N)
print("Severity range: %.4f .. %.4f" % (smin, smax))
print("\nTop 5 beaches by severity:")
for i in order[:5]:
    print("  %-22s %.4f" % (beaches[i], S[i]))
print("\nLowest severity beach:")
print("  %-22s %.4f" % (beaches[order[-1]], S[order[-1]]))

cat_totals = {c: 0.0 for c in CATEGORY_SEVERITY}
for j, meta in enumerate(plastic_metadata):
    for c in meta["categories"]:
        cat_totals[c] += float(avg_plastics[:, j].sum())
print("\nTotal (avg) items per category across all beaches:")
for c, v in sorted(cat_totals.items(), key=lambda kv: -kv[1]):
    print("  %-22s %.1f" % (c, v))

print("\nSaved:", OUT_TOP3)
print("Saved:", OUT_SEVERITY)

# ---- Static preview thumbnail for the about page ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PREVIEW = r"c:\Users\ishir\Desktop\Portfolio\images\scotland_severity_preview.png"
fig, ax = plt.subplots(figsize=(8, 6.5))
for i in range(len(beaches)):
    norm_s = (S[i] - smin) / (smax - smin) if smax > smin else 0.0
    ax.scatter(
        coords[i][1], coords[i][0],
        s=120 + 500 * norm_s,
        color=cmap(norm_s),
        edgecolors="white", linewidths=0.6, zorder=3,
    )
for i in order[:3]:
    ax.annotate(
        beaches[i], (coords[i][1], coords[i][0]),
        textcoords="offset points", xytext=(8, 6), fontsize=8, color="#222",
    )
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Plastic pollution severity across Scottish beaches")
sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=smin, vmax=smax))
sm.set_array([])
cb = plt.colorbar(sm, ax=ax)
cb.set_label("Severity score")
ax.grid(True, linestyle="--", alpha=0.3)
fig.tight_layout()
fig.savefig(PREVIEW, dpi=150)
print("Saved:", PREVIEW)

