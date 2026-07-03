/* ============================================================
   Ansari Sami — Front-end Recreation
   Vanilla JS: header scroll behavior, nav overlay, reveal-on-scroll,
   image fade-in, draggable sliders, filter bullets.
   ============================================================ */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", init);

  function init() {
    document.body.classList.remove("is-preload");
    initHeader();
    initNavOverlay();
    initRevealOnScroll();
    initImageFade();
    initSliders();
    initFilters();
    initYear();
  }

  /* ---------------- Header show/hide + solid state ---------------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    var subNav = document.querySelector("[data-sub-nav-bar]");
    if (!header) return;
    var lastY = window.scrollY;
    var ticking = false;

    function update() {
      var y = window.scrollY;
      if (y > 40) {
        header.classList.add("is-solid");
      } else {
        header.classList.remove("is-solid");
      }
      var headerHidden = y > lastY && y > 160;
      if (headerHidden) {
        header.classList.add("is-hidden");
      } else {
        header.classList.remove("is-hidden");
      }
      if (subNav) {
        if (y > 240) {
          subNav.classList.add("is-visible");
        } else {
          subNav.classList.remove("is-visible");
        }
        subNav.classList.toggle("is-docked", headerHidden);
      }
      lastY = y;
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    });
    update();
  }

  /* ---------------- Fullscreen nav overlay ---------------- */
  function initNavOverlay() {
    var openBtns = document.querySelectorAll("[data-nav-open]");
    var closeBtns = document.querySelectorAll("[data-nav-close]");
    var overlay = document.querySelector(".nav-overlay");
    if (!overlay) return;

    openBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        overlay.classList.add("is-open");
        document.documentElement.style.overflow = "hidden";
      });
    });
    closeBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        overlay.classList.remove("is-open");
        document.documentElement.style.overflow = "";
      });
    });
    overlay.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        overlay.classList.remove("is-open");
        document.documentElement.style.overflow = "";
      });
    });
  }

  /* ---------------- Reveal-on-scroll ---------------- */
  function initRevealOnScroll() {
    var items = document.querySelectorAll(".reveal, .reveal-fade, .reveal-scale");
    if (!("IntersectionObserver" in window) || !items.length) {
      items.forEach(function (el) { el.classList.add("is-inview"); });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-inview");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------------- Image fade-in on load ---------------- */
  function initImageFade() {
    var imgs = document.querySelectorAll("img[data-fade]");
    imgs.forEach(function (img) {
      if (img.complete && img.naturalWidth > 0) {
        img.classList.add("is-loaded");
      } else {
        img.addEventListener("load", function () { img.classList.add("is-loaded"); });
        img.addEventListener("error", function () { img.classList.add("is-loaded"); });
      }
    });
  }

  /* ---------------- Draggable / arrow sliders ---------------- */
  function initSliders() {
    document.querySelectorAll("[data-slider]").forEach(function (root) {
      var track = root.querySelector(".slider__track");
      if (!track) return;
      var prevBtns = root.querySelectorAll('[data-slider-prev]');
      var nextBtns = root.querySelectorAll('[data-slider-next]');
      var progressBar = root.querySelector(".slider__progress-bar");

      var isDown = false, startX, scrollLeft;

      track.addEventListener("pointerdown", function (e) {
        isDown = true;
        track.classList.add("is-dragging");
        startX = e.pageX - track.offsetLeft;
        scrollLeft = track.scrollLeft;
        track.setPointerCapture(e.pointerId);
      });
      track.addEventListener("pointermove", function (e) {
        if (!isDown) return;
        e.preventDefault();
        var x = e.pageX - track.offsetLeft;
        var walk = (x - startX) * 1.2;
        track.scrollLeft = scrollLeft - walk;
      });
      ["pointerup", "pointerleave", "pointercancel"].forEach(function (evt) {
        track.addEventListener(evt, function () {
          isDown = false;
          track.classList.remove("is-dragging");
        });
      });

      function scrollByCard(dir) {
        var card = track.querySelector("article");
        var amount = card ? card.getBoundingClientRect().width + 10 : 300;
        track.scrollBy({ left: dir * amount, behavior: "smooth" });
      }
      prevBtns.forEach(function (b) { b.addEventListener("click", function () { scrollByCard(-1); }); });
      nextBtns.forEach(function (b) { b.addEventListener("click", function () { scrollByCard(1); }); });

      if (progressBar) {
        track.addEventListener("scroll", function () {
          var max = track.scrollWidth - track.clientWidth;
          var pct = max > 0 ? track.scrollLeft / max : 0;
          progressBar.style.transform = "scaleX(" + Math.max(0.08, pct) + ")";
        });
      }

      // Click-to-navigate on cards with data-url (drag vs click distinguishing)
      var dragDistance = 0;
      track.addEventListener("pointerdown", function (e) { dragDistance = 0; });
      track.addEventListener("pointermove", function (e) { if (isDown) dragDistance += Math.abs(e.movementX || 0); });
      track.querySelectorAll("[data-url]").forEach(function (el) {
        el.style.cursor = "pointer";
        el.addEventListener("click", function () {
          if (dragDistance < 6) {
            window.location.href = el.getAttribute("data-url");
          }
        });
      });
    });
  }

  /* ---------------- Filter bullets (communities / real-estate index) ---------------- */
  function initFilters() {
    document.querySelectorAll("[data-filter-group]").forEach(function (group) {
      var buttons = group.querySelectorAll(".filt-bullet");
      var targetSelector = group.getAttribute("data-filter-group");
      var items = targetSelector ? document.querySelectorAll(targetSelector + " [data-region]") : [];

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          buttons.forEach(function (b) { b.classList.remove("is-active"); });
          btn.classList.add("is-active");
          var val = btn.getAttribute("data-value");
          items.forEach(function (item) {
            if (!val || val === "all" || item.getAttribute("data-region") === val) {
              item.style.display = "";
            } else {
              item.style.display = "none";
            }
          });
        });
      });
    });
  }

  function initYear() {
    var el = document.querySelector("[data-year]");
    if (el) el.textContent = new Date().getFullYear();
  }
})();
