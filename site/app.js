// Local times, search filters and kind toggles for the guide archive.
(function () {
  var pad = function (n) { return String(n).padStart(2, "0"); };
  document.querySelectorAll("time[datetime]").forEach(function (el) {
    var d = new Date(el.getAttribute("datetime"));
    if (isNaN(d)) return;
    var date = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
    var time = pad(d.getHours()) + ":" + pad(d.getMinutes());
    if (el.classList.contains("date")) {
      // Day headings are UTC dates; label them without shifting the day.
      el.textContent = new Date(el.getAttribute("datetime")).toLocaleDateString(undefined,
        { weekday: "long", year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
    } else if (el.classList.contains("time")) {
      el.textContent = time;
    } else if (el.classList.contains("short")) {
      el.textContent = date.slice(5) + " " + time;
    } else {
      el.textContent = date + " " + time;
    }
  });

  var kinds = document.querySelectorAll(".kinds input");
  function apply() {
    var box = document.querySelector("input[data-filter]");
    if (!box) return;
    var q = box.value.trim().toLowerCase();
    var on = {};
    kinds.forEach(function (k) { on[k.value] = k.checked; });
    document.querySelectorAll(box.getAttribute("data-filter")).forEach(function (li) {
      var kind = li.getAttribute("data-kind");
      var show = (!q || (li.getAttribute("data-q") || "").indexOf(q) !== -1) && (!kind || on[kind] !== false);
      li.hidden = !show;
    });
    document.querySelectorAll("section.day").forEach(function (s) {
      s.hidden = !s.querySelector("li:not([hidden])");
    });
  }
  document.querySelectorAll("input[data-filter]").forEach(function (b) { b.addEventListener("input", apply); });
  kinds.forEach(function (k) { k.addEventListener("change", apply); });
  apply();

  // Scale artboard previews to their card width.
  function fit() {
    document.querySelectorAll(".board .frame, .thumb").forEach(function (box) {
      var host = box.closest(".board") || box;
      var w = parseFloat(getComputedStyle(host).getPropertyValue("--w")) || 794;
      var f = box.querySelector("iframe");
      if (f) f.style.transform = "scale(" + box.clientWidth / w + ")";
    });
  }
  window.addEventListener("resize", fit);
  fit();

  var cur = document.querySelector(".wayback [aria-current]");
  if (cur) cur.scrollIntoView({ inline: "center", block: "nearest" });
})();
