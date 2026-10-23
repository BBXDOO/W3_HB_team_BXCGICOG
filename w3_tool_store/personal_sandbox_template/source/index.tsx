
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// The Android package bundles its own web assets. Chrome's offline cache is only
// needed by the browser/PWA edition and would otherwise shadow APK updates.
if (import.meta.env.PROD && location.hostname !== 'appassets.androidplatform.net' && 'serviceWorker' in navigator) {
  let refreshing = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (refreshing) return;
    refreshing = true;
    window.location.reload();
  });
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js?v=32`, { updateViaCache: 'none' }).then(registration => {
      // Check the installed offline shell on every online launch, including Chrome home-screen launches.
      if (navigator.onLine) registration.update().catch(() => {});
    }).catch(() => {
      // The application still works without the offline cache.
    });
  });
}
