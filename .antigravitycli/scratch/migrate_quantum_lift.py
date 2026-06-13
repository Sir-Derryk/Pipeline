import os
import re

# Paths to the layout files
base_dir = r"D:\My repositories\Pipeline"
list_html_path = os.path.join(base_dir, "user-docs", "hugo-site", "layouts", "_default", "list.html")
single_html_path = os.path.join(base_dir, "user-docs", "hugo-site", "layouts", "_default", "single.html")

def migrate_file(filepath):
    print(f"Migrating: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Define color replacements
    # Orange-red gradient and primary highlights to Quantum Lift
    replacements = {
        # Primary accent #ff3100 -> Electric Cyan #06B6D4
        "#ff3100": "#06B6D4",
        "ff3100": "06B6D4",
        # Secondary coral #ff6b4a -> Quantum Purple #8B5CF6
        "#ff6b4a": "#8B5CF6",
        "ff6b4a": "8B5CF6",
        # Very light orange background #fff0eb -> Very light cyan #ecfeff or light purple #f5f3ff
        "#fff0eb": "#ecfeff",
        # Orange/coral border #ffd0c4 -> Light cyan border #cffafe
        "#ffd0c4": "#cffafe",
    }

    # Perform exact replacements
    for src, dst in replacements.items():
        content = content.replace(src, dst)

    # Inject terminal / variable highlight rules into the style tag in list.html and single.html
    custom_syntax_highlight_rules = """
        /* Quantum Lift custom terminal and code variable highlighting (REQ-API-QL) */
        code, pre, .prose pre code {
            font-family: 'JetBrains Mono', monospace !important;
        }
        /* Highlight variables in angle brackets <variable> as neon lime */
        .token.variable, .token.attr-value, .token.string {
            color: #bef264 !important; /* Neon lime */
        }
        /* Flags/options highlighting (Quantum Purple) */
        .token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string, .token.variable {
            color: #8B5CF6 !important;
        }
        /* Active links / hover highlights */
        a {
            color: #06B6D4;
        }
        a:hover {
            color: #8B5CF6;
        }
    """

    # Let's append this CSS snippet right before </style>
    content = content.replace("</style>", custom_syntax_highlight_rules + "\n    </style>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully migrated {filepath}")

# Execute migrations
migrate_file(list_html_path)
migrate_file(single_html_path)
print("Quantum Lift migration completed for Hugo Layouts!")
