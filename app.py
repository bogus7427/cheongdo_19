from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

TRAVEL_STYLES = {
    "activity": "액티비티",
    "healing": "힐링",
    "photo": "사진 명소",
}

ATTRACTIONS = [
    {
        "name": "청도 와인터널",
        "description": "오래된 터널의 서늘한 공기와 은은한 조명이 어우러져 여유롭게 둘러보기 좋은 곳이에요.",
        "tags": ["실내 산책", "와인", "레트로 분위기"],
        "personalities": ["E", "I"],
        "purposes": ["healing", "photo"],
        "emoji": "🍷",
    },
    {
        "name": "청도 프로방스",
        "description": "알록달록한 건물과 빛으로 꾸민 공간을 배경으로 산책하고 사진을 남겨 보세요.",
        "tags": ["야경", "포토존", "산책"],
        "personalities": ["E", "I"],
        "purposes": ["photo", "healing"],
        "emoji": "✨",
    },
    {
        "name": "군파크 루지",
        "description": "청도의 풍경을 바라보며 루지를 타고 시원하게 달리는 활동적인 코스예요.",
        "tags": ["루지", "스피드", "야외 활동"],
        "personalities": ["E"],
        "purposes": ["activity"],
        "emoji": "🏎️",
    },
    {
        "name": "운문사",
        "description": "산자락의 고즈넉한 사찰을 천천히 걸으며 자연 속에서 마음을 쉬어 가기 좋아요.",
        "tags": ["사찰", "숲길", "고요한 시간"],
        "personalities": ["I", "E"],
        "purposes": ["healing", "photo"],
        "emoji": "🌿",
    },
    {
        "name": "새마을운동발상지 기념공원",
        "description": "전시와 야외 공간을 둘러보며 청도의 역사와 이야기를 알아볼 수 있어요.",
        "tags": ["역사", "전시", "야외 산책"],
        "personalities": ["I", "E"],
        "purposes": ["activity", "healing"],
        "emoji": "🏡",
    },
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/recommendations", methods=["POST"])
def recommend():
    data = request.get_json(silent=True) or {}
    personality = data.get("personality")
    purpose = data.get("purpose")

    if personality not in ("E", "I"):
        return jsonify({"error": "성향을 선택해 주세요."}), 400
    if purpose not in TRAVEL_STYLES:
        return jsonify({"error": "여행 목적을 선택해 주세요."}), 400

    ranked = sorted(
        ATTRACTIONS,
        key=lambda place: (
            purpose in place["purposes"],
            personality in place["personalities"],
        ),
        reverse=True,
    )
    recommendations = [
        {**place, "matched": purpose in place["purposes"]}
        for place in ranked[:2]
    ]

    route = [place["name"] for place in recommendations]
    return jsonify(
        {
            "personality": personality,
            "purpose": TRAVEL_STYLES[purpose],
            "recommendations": recommendations,
            "route": route,
            "route_description": " → ".join(route),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
