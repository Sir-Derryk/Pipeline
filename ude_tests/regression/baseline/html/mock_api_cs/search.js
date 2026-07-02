// engine/ude/templates/css/default/search.js
// Client-side real-time search filtering on #sidebarSearch input.
// All comments in English.

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("sidebarSearch");
    if (!searchInput) return;

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        const items = document.querySelectorAll("#toctree .OdaDocTOCItem");

        if (query === "") {
            // Restore default view: remove overrides and collapse elements normally
            items.forEach(item => {
                item.style.display = "";
                const row = item.querySelector(".OdaDocTOCRow");
                const toggle = item.querySelector(".OdaDocTOCToggle");
                if (row && toggle) {
                    const activeRow = item.querySelector(".OdaDocTOCRow.active");
                    if (activeRow || row.classList.contains("active")) {
                        item.classList.add("expanded");
                        toggle.textContent = "▼";
                    } else {
                        item.classList.remove("expanded");
                        toggle.textContent = "▶";
                    }
                }
            });
            return;
        }

        // Search mode: Filter elements and auto-expand matching hierarchies
        items.forEach(item => {
            item.style.display = "none";
            item.classList.remove("expanded");
            const toggle = item.querySelector(".OdaDocTOCToggle");
            if (toggle) toggle.textContent = "▶";
        });

        // Traverse and show matches + their ancestors
        items.forEach(item => {
            const labelEl = item.querySelector(".OdaDocTOCLabel");
            if (labelEl) {
                const labelText = labelEl.textContent.toLowerCase();
                if (labelText.includes(query)) {
                    item.style.display = "";
                    
                    let parent = item.parentElement;
                    while (parent && parent.id !== "toctree") {
                        if (parent.classList.contains("OdaDocTOCItem")) {
                            parent.style.display = "";
                            parent.classList.add("expanded");
                            const parentToggle = parent.querySelector(".OdaDocTOCToggle");
                            if (parentToggle) parentToggle.textContent = "▼";
                        }
                        parent = parent.parentElement;
                    }
                }
            }
        });
    });
});
