// Paste into DevTools Console on the HTTPS site's own page, after starting capture.
// Use an ordinary public page you control or have permission to test.
Promise.all(Array.from({length: 6}, (_, i) =>
    fetch(`/?cyl57=${i}`, {cache: "no-store"})
        .then(response => response.text())
)).then(results => console.log("Completed requests:", results.length));
