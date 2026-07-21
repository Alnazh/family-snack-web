// tombol tambah kurang jumlah pada input qty
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-qty-minus]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const input = document.getElementById(btn.dataset.qtyMinus);
      const val = parseInt(input.value) || 1;
      input.value = val > 1 ? val - 1 : 1;
    });
  });

  document.querySelectorAll("[data-qty-plus]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const input = document.getElementById(btn.dataset.qtyPlus);
      const val = parseInt(input.value) || 1;
      input.value = val + 1;
    });
  });

  // validasi bootstrap bawaan untuk form checkout dan kontak
  const forms = document.querySelectorAll(".needs-validation");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });
});
