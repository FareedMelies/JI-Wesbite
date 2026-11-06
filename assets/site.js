  // Paste real links here. Anything left blank shows as an inactive chip.
  var LINKS = { donate: "", instagram: "https://www.instagram.com/jasmineinitiative/", tiktok: "https://www.tiktok.com/@jasmineinitiative" };
  var SOCIAL = [["instagram","Instagram"],["tiktok","TikTok"]];

  document.querySelectorAll("[data-socials]").forEach(function(el){
    SOCIAL.forEach(function(s){
      var url = LINKS[s[0]], n;
      if (url) { n = document.createElement("a"); n.href = url; n.target = "_blank"; n.rel = "noopener noreferrer"; }
      else { n = document.createElement("span"); n.className = "is-off"; n.setAttribute("aria-disabled","true"); n.title = "Link coming soon"; }
      n.classList.add("chip");
      n.textContent = s[1];
      el.appendChild(n);
    });
  });

  document.querySelectorAll("[data-donate]").forEach(function(el){
    var n;
    if (LINKS.donate) { n = document.createElement("a"); n.href = LINKS.donate; n.target = "_blank"; n.rel = "noopener noreferrer"; n.className = "btn"; n.textContent = "Donate now →"; }
    else { n = document.createElement("span"); n.className = "btn is-off"; n.setAttribute("aria-disabled","true"); n.textContent = "Online giving opens soon"; }
    el.replaceWith(n);
  });

  document.querySelectorAll("[data-follow]").forEach(function(el){
    var n;
    if (LINKS.instagram) { n = document.createElement("a"); n.href = LINKS.instagram; n.target = "_blank"; n.rel = "noopener noreferrer"; n.className = "btn"; n.textContent = "Follow along on Instagram →"; }
    else { n = document.createElement("span"); n.className = "btn is-off"; n.setAttribute("aria-disabled","true"); n.textContent = "Follow along"; }
    el.replaceWith(n);
  });

  // Estimate inputs. 50 L per person per day is the WHO intermediate-access figure (water piped to the home).
  var WELLS = [{ done: "2026-10-20", people: 6 }, { done: "2026-10-25", people: 2 }];
  var LPCD = 50;
  function paintLiters(){
    var now = Date.now(), total = 0;
    WELLS.forEach(function(w){
      var start = new Date(w.done + "T00:00:00").getTime();
      total += w.people * LPCD * Math.max(0, (now - start) / 86400000);
    });
    var el = document.getElementById("liters");
    if (el) el.textContent = Math.floor(total).toLocaleString("en-US");
  }
  paintLiters();
  setInterval(paintLiters, 60000);

  // Contact form posts to a Google Apps Script web app (runs in our own Google account). Paste its URL here.
  var CONTACT_ENDPOINT = "";
  var cf = document.querySelector("[data-contact]");
  if (cf) {
    var cfOff = document.querySelector("[data-contact-off]");
    if (!CONTACT_ENDPOINT) { cf.hidden = true; if (cfOff) cfOff.hidden = false; }
    var cfT = cf.querySelector('[name="t"]'); if (cfT) cfT.value = String(Date.now());
    var cfS = cf.querySelector(".cform-status"), cfB = cf.querySelector("button[type=submit]");
    function cfSay(msg, html){ cfS.hidden = false; if (html) cfS.innerHTML = msg; else cfS.textContent = msg; }
    cf.addEventListener("submit", function(e){
      e.preventDefault();
      var d = new FormData(cf), name = (d.get("name")||"").trim(), email = (d.get("email")||"").trim(), msg = (d.get("message")||"").trim();
      if (!name || !msg || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { cfSay("Please fill in your name, a valid email, and a message."); return; }
      cfB.disabled = true; cfSay("Sending...");
      fetch(CONTACT_ENDPOINT, { method: "POST", mode: "no-cors", body: new URLSearchParams(d) })
        .then(function(){ cf.reset(); if (cfT) cfT.value = String(Date.now()); cfSay("Thank you. Your message is on its way to our inbox."); })
        .catch(function(){ cfSay('Something went wrong. Please email <a href="mailto:hello@jasmineinitiative.org">hello@jasmineinitiative.org</a>.', true); })
        .then(function(){ cfB.disabled = false; });
    });
  }


  var btn = document.getElementById("menuBtn"), menu = document.getElementById("menu");
  function setMenu(open){
    menu.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = open ? "Close" : "Menu";
    document.body.classList.toggle("menu-open", open);
  }
  btn.addEventListener("click", function(){ setMenu(menu.hidden); });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") setMenu(false); });
