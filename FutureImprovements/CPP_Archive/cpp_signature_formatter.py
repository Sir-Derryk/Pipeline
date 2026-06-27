# FutureImprovements/CPP_Archive/cpp_signature_formatter.py
# Archived from engine/ude/formatters/signatures.py — CppSignatureFormatter class.
# Not part of the active Python SDK pipeline. Retained for future C++ support.
# All documentation, docstrings, and code comments are strictly in English.

import re
from typing import List
from ude.models import ClassEntity, NamespaceEntity, ParameterField
from ude.formatters.signatures import BaseSignatureFormatter


class CppSignatureFormatter(BaseSignatureFormatter):
    """C++ specific signature and naming formatter strategy."""

    def format_class_declaration(self, cls: ClassEntity) -> str:
        kw = "struct" if cls.entity_type.lower() == "struct" else "class"
        base = f" : public {cls.base_class}" if cls.base_class else ""
        lines = [f"{kw} {cls.name}{base} {{"]
        for field in cls.fields:
            lines.append(f"  {field};")
        lines.append("};")
        return "\n".join(lines)

    def format_namespace_declaration(self, ns: NamespaceEntity) -> str:
        return f"namespace {ns.name} {{\n  // Namespace containing classes and types\n}};"

    def format_scope_name(self, ns_name: str) -> str:
        return ns_name if ns_name else "Global"

    def format_fully_qualified_name(self, fqn: str) -> str:
        return fqn if fqn else ""

    def format_entity_type(self, entity_type: str) -> str:
        return entity_type.lower()

    def format_fallback_method_signature(
        self,
        name: str,
        parameters: List[ParameterField],
        return_type: str,
        is_static: bool
    ) -> str:
        param_str = ", ".join(f"{p.type} {p.name}".strip() for p in parameters)
        prefix = "static " if is_static else ""
        ret = f"{return_type} " if return_type else ""
        sig = f"{prefix}{ret}{name}({param_str})"
        return re.sub(r"\s+", " ", sig).strip()
