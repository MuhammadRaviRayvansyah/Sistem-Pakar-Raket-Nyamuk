import json

def tanya(fakta):
    jawab = input(f"Apakah {fakta}? (y/t) > ").strip().lower()
    return jawab == "y"

def syarat_terpenuhi(aturan, memori):
    if aturan["mode"] == "dan":
        return all(f in memori for f in aturan["jika"])
    return any(f in memori for f in aturan["jika"])

def forward_chaining(kb, memori, alasan):
    siklus = 1

    while True:
        cocok = [
            a for a in kb["aturan"]
            if syarat_terpenuhi(a, memori) and a["maka"] not in memori
        ]

        if not cocok:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break

        aturan = cocok[0]
        hasil = aturan["maka"]
        memori.add(hasil)
        alasan[hasil] = aturan

        syarat = ", ".join(aturan["jika"])
        print(f"Siklus {siklus}: {aturan['id']} -> {hasil}")

        siklus += 1

    return memori, alasan

def tampilkan_kesimpulan(kb, memori, alasan):
    kesimpulan = [
        "raket perlu diperiksa pengisiannya",
        "efektivitas raket menurun",
        "perlu servis atau penggantian",
        "hentikan penggunaan segera"
    ]

    hasil = [k for k in kesimpulan if k in memori]

    print("\nKesimpulan:")
    if not hasil:
        print("Tidak ada kesimpulan akhir. Periksa kondisi baterai, tombol, kabel, dan jaring raket.")
    else:
        for k in hasil:
            print(f"- {k}")

    print("\nAlasan:")
    for k in hasil:
        a = alasan[k]
        print(f"{k} <- {a['id']} ({', '.join(a['jika'])})")

    print("\nCatatan batas keberlakuan:")
    print(kb["batas"])

def main():
    with open("kb_raket_nyamuk.json", "r", encoding="utf-8") as file:
        kb = json.load(file)

    print(kb["judul"])
    print("Jawab y/t.\n")

    memori = set()
    alasan = {}

    for fakta in kb["fakta"]:
        if tanya(fakta):
            memori.add(fakta)

    print("\nFakta awal:", ", ".join(sorted(memori)) if memori else "tidak ada")
    print()

    memori, alasan = forward_chaining(kb, memori, alasan)
    tampilkan_kesimpulan(kb, memori, alasan)

if __name__ == "__main__":
    main()