def render_markdown(pr, state, score, reasons, metrics, recs):
    emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

    bar = "🟩🟩"
    bar += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    bar += "🟩"
    bar += "🟨" if state == "yellow" else "🟥" if state == "red" else "🟩"
    bar += "🟩"

    md = []
    md.append("## 🔍 IGET PR Analysis")
    md.append(f"### PR #{pr}\n")

    md.append("### 📊 Progress")
    md.append("[██████████] 100%\n")

    md.append("### 🔗 Flow")
    md.append("A → B → C → D → E → F\n")

    md.append("### 🧩 State")
    md.append(bar + "\n")

    md.append("### 📋 Summary")
    for r in reasons:
        md.append(f"- {r}")

    md.append("\n### 🎯 Impact")
    md.append(f"{emoji[state]} {state} (score: {score})")

    md.append("\n### 🧠 Recommend")
    for r in recs:
        md.append(f"- {r}")

    md.append("\n### 📂 Data")
    md.append(f"- files: {metrics['files']}")
    md.append(f"- changes: {metrics['changes']}")
    md.append(f"- tests: {metrics['tests']}")

    result = "✅ ผ่าน" if state != "red" else "❌ มีความเสี่ยง"
    md.append("\n### 🏁 Result")
    md.append(result)

    return "\n".join(md)
