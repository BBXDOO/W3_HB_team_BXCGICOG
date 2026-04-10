def render(data):
    emoji = {
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴"
    }

    # ----------------------
    # PROGRESS BAR
    # ----------------------
    bar = "".join([
        "🟩" if s == "green"
        else "🟨" if s == "yellow"
        else "🟥"
        for s in data["states"]
    ])

    percent = f"{data['progress']:.2f}"

    # ----------------------
    # BUILD MARKDOWN
    # ----------------------
    output = []

    output.append("# 🔍 IGET PR Analysis")
    output.append(f"## 🧾 PR: {data['pr']}")

    # B + C
    output.append("\n## 📊 Progress")
    output.append(f"{bar} {percent}%")

    # Flow
    output.append("\n## 🔗 Flow")
    output.append(" → ".join(data["flow"]))

    # Summary (D/E)
    output.append("\n## 📋 SUMMARY")
    for i in data["issues"]:
        output.append(f"- {i['node']} → {emoji[i['state']]} {i['state']}")

    # Impact (F + G)
    output.append("\n## 🎯 IMPACT")
    for i in data["issues"]:
        output.append(f"- {i['node']} → {i['impact']}")

    # Result
    if any(i["state"] == "red" for i in data["issues"]):
        output.append("\n## 🏁 RESULT")
        output.append("❌ มีความเสี่ยง")
    else:
        output.append("\n## 🏁 RESULT")
        output.append("✅ สำเร็จ")

    return "\n".join(output)
