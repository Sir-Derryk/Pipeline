// engine/ude/templates/css/default/oda_search.js
// Client-side redirection to Docomatic search page.
// All comments in English.

function odaSearch() {
    const value = document.getElementById('odaSearchInput').value;

    if (value !== '') {
        const section = window.location.pathname.replace(/^\/([^\/]*).*$/, "$1");
        const url = '/search?section=' + section + '&query=' + encodeURI(value);
        window.open(url, '_blank');
    }
}
