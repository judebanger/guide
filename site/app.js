// guide archive: local times, session filter, step timeline, preview scaling.
(function () {
  var pad = function (n) { return String(n).padStart(2, "0"); };
  document.querySelectorAll("time[datetime]").forEach(function (el) {
    var d = new Date(el.getAttribute("datetime"));
    if (isNaN(d)) return;
    var date = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
    var time = pad(d.getHours()) + ":" + pad(d.getMinutes());
    if (el.classList.contains("day")) {
      el.textContent = d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric", timeZone: "UTC" });
    } else if (el.classList.contains("time")) {
      el.textContent = time;
    } else {
      el.textContent = date + " " + time;
    }
  });

  // Session list filter.
  var box = document.querySelector("input[data-filter]");
  if (box) box.addEventListener("input", function () {
    var q = box.value.trim().toLowerCase();
    document.querySelectorAll(box.getAttribute("data-filter")).forEach(function (el) {
      el.hidden = !!q && el.textContent.toLowerCase().indexOf(q) === -1;
    });
  });

  // Scale each live preview to its frame's width (also when a hidden step is shown).
  function fit(frame) {
    var host = frame.closest("[style*='--w']") || frame;
    var w = parseFloat(getComputedStyle(host).getPropertyValue("--w")) || 794;
    var f = frame.querySelector("iframe");
    if (f && frame.clientWidth) f.style.transform = "scale(" + frame.clientWidth / w + ")";
  }
  var ro = "ResizeObserver" in window ? new ResizeObserver(function (entries) {
    entries.forEach(function (e) { fit(e.target); });
  }) : null;
  document.querySelectorAll(".board .frame").forEach(function (fr) {
    fit(fr);
    if (ro) ro.observe(fr);
  });
  if (!ro) window.addEventListener("resize", function () {
    document.querySelectorAll(".board .frame").forEach(fit);
  });

  // Step timeline on a session page.
  var panels = document.querySelector(".panels");
  if (!panels) return;
  var steps = Array.prototype.slice.call(panels.querySelectorAll(".step"));
  var ticks = Array.prototype.slice.call(document.querySelectorAll(".tick"));
  var current = -1;
  function show(n, push) {
    n = Math.max(0, Math.min(steps.length - 1, n));
    if (n === current) return;
    current = n;
    steps.forEach(function (s, i) { s.hidden = i !== n; });
    ticks.forEach(function (t, i) {
      if (i === n) {
        t.setAttribute("aria-current", "step");
        var track = t.closest(".track");
        track.scrollLeft = t.offsetLeft - track.clientWidth / 2 + t.offsetWidth / 2;
      } else t.removeAttribute("aria-current");
    });
    document.querySelectorAll(".nav").forEach(function (b) {
      b.disabled = (b.dataset.dir === "-1" && n === 0) || (b.dataset.dir === "1" && n === steps.length - 1);
    });
    if (push) history.replaceState(null, "", "#" + (n + 1));
    steps[n].querySelectorAll(".board .frame").forEach(fit);
  }
  ticks.forEach(function (t) {
    t.addEventListener("click", function () { show(+t.dataset.step, true); });
  });
  document.querySelectorAll(".nav").forEach(function (b) {
    b.addEventListener("click", function () { show(current + (+b.dataset.dir), true); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input, textarea")) return;
    if (e.key === "ArrowLeft") show(current - 1, true);
    if (e.key === "ArrowRight") show(current + 1, true);
  });
  var fromHash = parseInt(location.hash.slice(1), 10);
  show(fromHash > 0 ? fromHash - 1 : +panels.dataset.default, false);
})();
