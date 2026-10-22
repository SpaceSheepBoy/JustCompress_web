/* PostHog 1.438.15: optional website analytics for Space Sheep Studio. */
(function () {
  'use strict';
  var site = location.hostname.indexOf('captions') !== -1 ? 'justcaptions' : 'justcompress';
  var key = 'spacesheep.analytics.v1';
  var blocked = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1';
  var client, loading = false, banner, choices;
  function preference(value) {
    try { if (value) localStorage.setItem(key, value); return localStorage.getItem(key); }
    catch (_) { return value || null; }
  }
  function safeUrl(value) {
    try { var url = new URL(value, location.origin); return url.origin + url.pathname; }
    catch (_) { return ''; }
  }
  function start() {
    if (blocked || client || loading || preference() !== 'allow') return;
    loading = true;
    var script = document.createElement('script');
    script.src = '/assets/vendor/posthog-1.438.15.js';
    script.onload = function () {
      loading = false;
      if (preference() !== 'allow') return;
      client = window.posthog.init('phc_nW8CSZb3fLQBKfiBtWNeVqbgzUFdBqmukxZDeLFoXZFT', {
        api_host: 'https://us.i.posthog.com',
        persistence: 'localStorage', cross_subdomain_cookie: false,
        person_profiles: 'never', autocapture: false,
        capture_pageview: false, capture_pageleave: false,
        disable_session_recording: true, disable_surveys: true,
        capture_exceptions: false, capture_performance: false,
        capture_heatmaps: false, disable_external_dependency_loading: true,
        advanced_disable_feature_flags: true,
        before_send: function (event) {
          if (blocked || preference() !== 'allow') return null;
          var props = event.properties || {};
          Object.keys(props).forEach(function (name) {
            if (/url|referrer/i.test(name) && typeof props[name] === 'string') props[name] = safeUrl(props[name]);
            if (/^\$?(initial_)?(utm_|gclid|fbclid|msclkid)/i.test(name) || name === '$set' || name === '$set_once') delete props[name];
          });
          props.site = site;
          return event;
        },
        loaded: function (posthog) {
          posthog.opt_in_capturing({ captureEventName: false });
          posthog.capture('$pageview', { site: site, $current_url: safeUrl(location.href) });
        }
      });
    };
    script.onerror = function () { loading = false; };
    document.head.appendChild(script);
  }
  function choose(value) {
    preference(value);
    banner.hidden = true;
    if (value === 'allow') start();
    else if (client) { client.opt_out_capturing(); client = null; }
  }
  function button(label, callback) {
    var el = document.createElement('button'); el.type = 'button'; el.textContent = label;
    el.addEventListener('click', callback); return el;
  }
  if (blocked) return;
  var style = document.createElement('style');
  style.textContent = '.ss-analytics{position:fixed;z-index:9999;box-sizing:border-box;color:#172033;background:#fff;border:1px solid #c7cbd1;border-radius:14px;box-shadow:0 4px 24px #0002;font:14px/1.5 system-ui,sans-serif;padding:16px}.ss-analytics[hidden]{display:none}.ss-analytics-banner{bottom:52px;left:16px;max-width:420px;width:calc(100% - 32px)}.ss-analytics button{font:inherit;color:#172033;background:#f0f1f3;border:1px solid #b5bac2;border-radius:7px;padding:7px 13px;margin:10px 8px 0 0;cursor:pointer}.ss-analytics a{color:#194eac;text-decoration:underline}.ss-analytics-choice{bottom:10px;left:16px;padding:5px 10px;cursor:pointer}';
  document.head.appendChild(style);
  banner = document.createElement('section'); banner.className = 'ss-analytics ss-analytics-banner';
  banner.setAttribute('aria-label', 'Optional website analytics');
  var text = document.createElement('div');
  text.textContent = 'Allow optional analytics? PostHog helps Space Sheep Studio understand page visits and download clicks. We do not record sessions, form contents, or your files. ';
  var policy = document.createElement('a');
  policy.href = 'https://justcompress.online/privacy/'; policy.textContent = 'Privacy policy';
  text.appendChild(policy); banner.appendChild(text);
  banner.appendChild(button('Reject', function () { choose('deny'); }));
  banner.appendChild(button('Allow analytics', function () { choose('allow'); }));
  choices = button('Privacy choices', function () { banner.hidden = !banner.hidden; });
  choices.className = 'ss-analytics ss-analytics-choice';
  document.body.appendChild(banner); document.body.appendChild(choices);
  banner.hidden = preference() === 'allow' || preference() === 'deny';
  start();
  document.addEventListener('click', function (event) {
    if (!client || preference() !== 'allow') return;
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var url = new URL(link.href, location.origin), type;
    if (url.hostname === 'apps.apple.com') type = 'app_store_click';
    else if (/\.(dmg|zip)$/i.test(url.pathname)) type = 'download_click';
    if (type) client.capture(type, { site: site, destination: safeUrl(url.href) });
  });
})();
