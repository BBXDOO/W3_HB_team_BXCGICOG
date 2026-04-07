def render(data):
    print("\n🔴 PR:", data["pr"])

    # B + C
    bar = "".join(["🟩" if s == "green" else "🟨" if s == "yellow" else "🟥" for s in data["states"]])
    print("Progress:", f"{data['progress']:.2f}%")
    print("Flow:", bar)

    # D
    print("\nFlow:")
    print(" → ".join(data["flow"]))

    # E
    print("\n📋 SUMMARY")
    for i in data["issues"]:
        print(f"- {i['node']} → {i['state']}")

    # F + G
    print("\n🎯 IMPACT")
    for i in data["issues"]:
        print(f"- {i['node']} → {i['impact']}")

    # RESULT
    if any(i["state"] == "red" for i in data["issues"]):
        print("\n❌ RESULT: มีความเสี่ยง")
    else:
        print("\n✅ RESULT: สำเร็จ")
