import re
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "family-snack-rahasia-2026"

# katalog produk disimpan langsung sebagai data python, tidak perlu database
PRODUCTS = [
    {"id": 1, "name": "Kripca Original", "category": "Kripca", "price": 15000, "rating": 4.9,
     "tag": "Original", "badge": "TERLARIS", "image": "kripca_original.jpg",
     "description": "Kripik kaca singkong tipis dan ekstra renyah dengan bumbu gurih klasik."},
    {"id": 2, "name": "Ghost Chili Kripca", "category": "Kripca", "price": 15000, "rating": 5.0,
     "tag": "Ekstra Pedas", "badge": None, "image": "kripca_ekstra_pedas.jpg",
     "description": "Bukan untuk yang penakut, dipadukan dengan serpihan cabai ghost pepper asli."},
    {"id": 3, "name": "Kripca Premium", "category": "Kripca", "price": 20000, "rating": 5.0,
     "tag": "Gurih", "badge": None, "image": "kripca_beranda.png",
     "description": "Versi premium kripca dengan lapisan bumbu yang lebih melimpah dan renyah maksimal."},
    {"id": 4, "name": "Kulit Ayam Krispy", "category": "Kulit & Usus", "price": 20000, "rating": 4.8,
     "tag": "Gurih", "badge": None, "image": "kulit.jpg",
     "description": "Kulit ayam krispy premium, dibumbui sempurna untuk camilan gurih terbaik."},
    {"id": 5, "name": "Usus Ayam Krispy", "category": "Kulit & Usus", "price": 18000, "rating": 4.7,
     "tag": "Pedas", "badge": None, "image": "usus.jpg",
     "description": "Digoreng hingga kecoklatan, usus krispy ini bikin ketagihan dan penuh rasa."},
    {"id": 6, "name": "Makroni Pedas", "category": "Makroni & Seblak", "price": 12000, "rating": 4.9,
     "tag": "Daun Jeruk", "badge": None, "image": "makroni.jpg",
     "description": "Makroni pedas yang dipadukan dengan aroma daun jeruk yang menyegarkan."},
    {"id": 7, "name": "Seblak Kering", "category": "Makroni & Seblak", "price": 12000, "rating": 4.6,
     "tag": "Pedas", "badge": None, "image": "seblak.jpg",
     "description": "Kerupuk seblak pedas tradisional dengan perpaduan kaya rempah khas Sunda."},
]


def find_product(product_id):
    # cari produk dari list berdasarkan id
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def get_cart():
    return session.get("cart", {})


def cart_details():
    # gabungkan data keranjang session dengan katalog produk
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        product = find_product(int(pid))
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return items, total


@app.route("/")
def home():
    featured = sorted(PRODUCTS, key=lambda p: p["rating"], reverse=True)[:4]
    return render_template("index.html", products=featured)


@app.route("/produk")
def produk():
    kategori = request.args.get("kategori", "Semua")
    cari = request.args.get("cari", "").strip().lower()

    hasil = PRODUCTS
    if kategori and kategori != "Semua":
        hasil = [p for p in hasil if p["category"] == kategori]
    if cari:
        hasil = [p for p in hasil if cari in p["name"].lower()]

    kategori_list = ["Semua", "Kripca", "Kulit & Usus", "Makroni & Seblak"]
    return render_template("products.html", products=hasil, kategori_list=kategori_list,
                            kategori_aktif=kategori, cari=request.args.get("cari", ""))


@app.route("/produk/<int:product_id>")
def produk_detail(product_id):
    product = find_product(product_id)
    if product is None:
        flash("Produk tidak ditemukan.", "error")
        return redirect(url_for("produk"))
    terkait = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product_id][:3]
    return render_template("product_detail.html", product=product, terkait=terkait)


@app.route("/tambah-keranjang/<int:product_id>", methods=["POST"])
def tambah_keranjang(product_id):
    qty = int(request.form.get("qty", 1))
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    session["cart"] = cart
    flash("Produk berhasil ditambahkan ke keranjang.", "success")
    return redirect(request.referrer or url_for("produk"))


@app.route("/hapus-keranjang/<int:product_id>", methods=["POST"])
def hapus_keranjang(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("keranjang"))


@app.route("/keranjang")
def keranjang():
    items, total = cart_details()
    return render_template("cart.html", items=items, total=total)


@app.route("/tentang-kami")
def tentang_kami():
    return render_template("about.html")


def validate_contact(name, email, subject, message):
    # validasi sederhana form kontak
    errors = []
    if len(name) < 3:
        errors.append("Nama lengkap minimal 3 karakter.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Format email tidak valid.")
    if not subject:
        errors.append("Subjek wajib dipilih.")
    if len(message) < 10:
        errors.append("Pesan minimal 10 karakter.")
    return errors


@app.route("/kontak", methods=["GET", "POST"])
def kontak():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        errors = validate_contact(name, email, subject, message)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("contact.html", form=request.form)

        flash("Pesan Anda berhasil dikirim, tim kami akan segera membalas.", "success")
        return redirect(url_for("kontak"))

    return render_template("contact.html", form={})


def validate_checkout(data):
    # validasi wajib untuk form checkout sesuai ketentuan tugas
    errors = []
    if len(data.get("full_name", "").strip()) < 3:
        errors.append("Nama penerima minimal 3 karakter.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", data.get("email", "")):
        errors.append("Format email tidak valid.")
    phone = data.get("phone", "").strip()
    if not re.match(r"^[0-9+]{9,15}$", phone):
        errors.append("Nomor telepon tidak valid, gunakan 9-15 digit angka.")
    if len(data.get("address", "").strip()) < 10:
        errors.append("Alamat pengiriman minimal 10 karakter.")
    if data.get("payment_method") not in ("transfer", "cod", "ewallet"):
        errors.append("Silakan pilih metode pembayaran.")
    return errors


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_details()
    if not items and request.method == "GET":
        flash("Keranjang Anda masih kosong, silakan pilih camilan dahulu.", "error")
        return redirect(url_for("produk"))

    if request.method == "POST":
        data = request.form
        errors = validate_checkout(data)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("checkout.html", items=items, total=total, form=data)

        # buat nomor pesanan sederhana dari nomor urut session, tanpa database
        order_number = session.get("last_order", 1000) + 1
        session["last_order"] = order_number

        order = {
            "id": order_number,
            "full_name": data["full_name"],
            "payment_method": data["payment_method"],
            "total": total,
        }
        session["last_order_items"] = items
        session["cart"] = {}
        return render_template("success.html", order=order, order_items=items)

    return render_template("checkout.html", items=items, total=total, form={})


@app.context_processor
def inject_cart_count():
    # supaya jumlah item keranjang bisa dipakai di semua halaman (navbar)
    cart = get_cart()
    return {"cart_count": sum(cart.values())}


if __name__ == "__main__":
    app.run(debug=True)
