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

  var ct = document.getElementById("colorToggle");
  if (ct) ct.addEventListener("click", function(){
    var on = document.getElementById("field").classList.toggle("color");
    ct.setAttribute("aria-checked", String(on));
  });

  var btn = document.getElementById("menuBtn"), menu = document.getElementById("menu");
  function setMenu(open){
    menu.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = open ? "Close" : "Menu";
    document.body.classList.toggle("menu-open", open);
  }
  btn.addEventListener("click", function(){ setMenu(menu.hidden); });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") setMenu(false); });
