/* Consentimiento de cookies + GA4 con Consent Mode v2
   cardiolopezclemente.com */
(function () {
  var GA_ID = 'G-E78Z4BSEDG';
  var KEY = 'clc-cookie-consent'; // 'granted' | 'denied'

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  // Consent Mode v2: todo denegado por defecto
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  function loadGA() {
    gtag('consent', 'update', { analytics_storage: 'granted' });
    if (document.getElementById('ga4-lib')) return;
    var s = document.createElement('script');
    s.id = 'ga4-lib';
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
  }

  function getConsent() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function setConsent(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  function hideBanner() {
    var b = document.getElementById('clc-cookies');
    if (b) b.remove();
  }

  function showBanner() {
    if (document.getElementById('clc-cookies')) return;

    var style = document.createElement('style');
    style.textContent =
      '#clc-cookies{position:fixed;bottom:16px;left:16px;right:16px;z-index:99999;' +
      'max-width:560px;margin:0 auto;background:#0f0f0f;color:#fff;' +
      'border-radius:16px;padding:22px 24px;box-shadow:0 16px 48px rgba(15,15,15,.35);' +
      'font-family:"DM Sans",-apple-system,sans-serif;font-size:.92rem;line-height:1.55}' +
      '#clc-cookies p{margin:0 0 16px;color:rgba(255,255,255,.85)}' +
      '#clc-cookies a{color:#fff;font-weight:600;text-decoration:underline}' +
      '#clc-cookies .clc-btns{display:flex;gap:10px;flex-wrap:wrap}' +
      '#clc-cookies button{cursor:pointer;border:none;border-radius:4px;' +
      'padding:11px 22px;font-family:inherit;font-size:.9rem;font-weight:600}' +
      '#clc-accept{background:#b80101;color:#fff}' +
      '#clc-accept:hover{background:#8b0000}' +
      '#clc-reject{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.4)!important}' +
      '#clc-reject:hover{border-color:#fff!important}';
    document.head.appendChild(style);

    var div = document.createElement('div');
    div.id = 'clc-cookies';
    div.setAttribute('role', 'dialog');
    div.setAttribute('aria-label', 'Aviso de cookies');
    div.innerHTML =
      '<p>Usamos cookies de análisis (Google Analytics) para entender cómo se usa la web y mejorarla. ' +
      'Solo se activan si las aceptas. Más información en la ' +
      '<a href="/legal/cookies.html">política de cookies</a>.</p>' +
      '<div class="clc-btns">' +
      '<button id="clc-accept" type="button">Aceptar</button>' +
      '<button id="clc-reject" type="button">Rechazar</button>' +
      '</div>';
    document.body.appendChild(div);

    document.getElementById('clc-accept').onclick = function () {
      setConsent('granted'); hideBanner(); loadGA();
    };
    document.getElementById('clc-reject').onclick = function () {
      setConsent('denied'); hideBanner();
    };
  }

  // Función global para revocar/cambiar desde cookies.html
  window.clcGestionarCookies = function () {
    try { localStorage.removeItem(KEY); } catch (e) {}
    showBanner();
  };

  var stored = getConsent();
  if (stored === 'granted') {
    loadGA();
  } else if (stored !== 'denied') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showBanner);
    } else {
      showBanner();
    }
  }
})();
