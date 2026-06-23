// engine/ude/templates/css/default/sidebar.js
// Offline-friendly standalone sidebar tree renderer and draggable splitter controller.
// All comments in English.

document.addEventListener("DOMContentLoaded", () => {
    const toctreeContainer = document.getElementById("toctree");
    if (!toctreeContainer) return;

    const navData = window.UDE_NAV_DATA;
    if (!navData) {
        toctreeContainer.innerHTML = "<p style='padding: 8px; color: red;'>Navigation data not found.</p>";
        return;
    }

    // Determine current page filename to set active menu item
    const currentPath = window.location.pathname;
    const currentFilename = currentPath.substring(currentPath.lastIndexOf("/") + 1) || "index.html";

    // Recursively build the HTML representation of the TOC
    function buildTree(nodes) {
        const ul = document.createElement("ul");
        ul.className = "OdaDocTOCList";

        nodes.forEach(node => {
            const li = document.createElement("li");
            li.className = "OdaDocTOCItem";
            
            const row = document.createElement("div");
            row.className = "OdaDocTOCRow";

            // Mark active if current page
            if (node.url === currentFilename) {
                row.classList.add("active");
            }

            const hasChildren = node.children && node.children.length > 0;
            if (hasChildren) {
                li.classList.add("node-type-group");
                
                const toggle = document.createElement("span");
                toggle.className = "OdaDocTOCToggle";
                toggle.textContent = "▶";
                
                row.appendChild(toggle);

                // Default expanded state if active or has active children
                function checkActive(n) {
                    if (n.url === currentFilename) return true;
                    if (n.children) {
                        return n.children.some(checkActive);
                    }
                    return false;
                }
                
                if (checkActive(node)) {
                    li.classList.add("expanded");
                    toggle.textContent = "▼";
                }

                // Toggle click behavior
                row.addEventListener("click", (e) => {
                    if (e.target === toggle) {
                        e.stopPropagation();
                        e.preventDefault();
                        li.classList.toggle("expanded");
                        toggle.textContent = li.classList.contains("expanded") ? "▼" : "▶";
                        return;
                    }
                    if (!node.url || node.url === "#" || node.url === "") {
                        li.classList.toggle("expanded");
                        toggle.textContent = li.classList.contains("expanded") ? "▼" : "▶";
                    }
                });
                
                toggle.addEventListener("click", (e) => {
                    e.stopPropagation();
                    li.classList.toggle("expanded");
                    toggle.textContent = li.classList.contains("expanded") ? "▼" : "▶";
                });
            } else {
                const spacer = document.createElement("span");
                spacer.className = "OdaDocTOCSpacer";
                row.appendChild(spacer);
            }

            // Create Label
            if (node.url && node.url !== "#" && node.url !== "") {
                const label = document.createElement("a");
                label.className = "OdaDocTOCLabel";
                label.href = node.url;
                label.textContent = node.label;
                row.appendChild(label);
            } else {
                const label = document.createElement("span");
                label.className = "OdaDocTOCLabel";
                label.textContent = node.label;
                row.appendChild(label);
            }

            li.appendChild(row);

            if (hasChildren) {
                const childUl = buildTree(node.children);
                li.appendChild(childUl);
            }

            ul.appendChild(li);
        });

        return ul;
    }

    // Render tree inside container
    toctreeContainer.innerHTML = "";
    const treeElement = buildTree(navData);
    toctreeContainer.appendChild(treeElement);

    // Auto-scroll the active row as high as possible inside the toctree container
    const activeRow = toctreeContainer.querySelector(".OdaDocTOCRow.active");
    if (activeRow) {
        let offset = 0;
        let curr = activeRow;
        while (curr && curr !== toctreeContainer) {
            offset += curr.offsetTop;
            curr = curr.offsetParent;
        }
        toctreeContainer.scrollTop = offset;
    }

    // Dynamic Panel Resize Splitter Implementation
    const splitter = document.querySelector(".OdaDocSplitter");
    const sidebar = document.querySelector(".OdaDocTOCPanel");

    if (splitter && sidebar) {
        // Load persisted width
        const savedWidth = localStorage.getItem("ude_sidebar_width");
        if (savedWidth) {
            sidebar.style.width = savedWidth + "px";
        }

        splitter.addEventListener("mousedown", (e) => {
            e.preventDefault();
            document.body.style.cursor = "col-resize";
            sidebar.classList.add("resizing");
            splitter.classList.add("dragging");

            const onMouseMove = (moveEvent) => {
                const newWidth = Math.max(180, Math.min(600, moveEvent.clientX));
                sidebar.style.width = newWidth + "px";
            };

            const onMouseUp = () => {
                document.body.style.cursor = "";
                sidebar.classList.remove("resizing");
                splitter.classList.remove("dragging");
                localStorage.setItem("ude_sidebar_width", sidebar.offsetWidth);
                document.removeEventListener("mousemove", onMouseMove);
                document.removeEventListener("mouseup", onMouseUp);
            };

            document.addEventListener("mousemove", onMouseMove);
            document.addEventListener("mouseup", onMouseUp);
        });
    }
});
