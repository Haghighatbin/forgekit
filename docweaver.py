#!/usr/bin/env python3
"""
Auto-docstring generator.

Usage:
    python auto_docstrings.py input_file.py output_file.py
"""

import ast
import argparse
from typing import Optional, List, Tuple
from garnishv2 import timeit


def ast_to_source(node: ast.AST) -> str:
    """
    Convert an AST node to source code using ast.unparse (Python 3.9+).
    Falls back to a simple repr if unparse is not available.
    """
    try:
        return ast.unparse(node)  # type: ignore[attr-defined]
    except Exception:
        return repr(node)

def extract_parameters(func: ast.FunctionDef) -> List[Tuple[str, Optional[str]]]:
    """
    Extract parameter names and type annotations (if present) from a function.

    Returns:
        List of (name, annotation_string_or_None).
    """
    params: List[Tuple[str, Optional[str]]] = []
    args = func.args

    # Positional-only args (Python 3.8+)
    for arg in getattr(args, "posonlyargs", []):
        annotation = ast_to_source(arg.annotation) if arg.annotation else None
        params.append((arg.arg, annotation))

    # Regular positional args
    for arg in args.args:
        annotation = ast_to_source(arg.annotation) if arg.annotation else None
        params.append((arg.arg, annotation))

    # *args
    if args.vararg:
        annotation = ast_to_source(args.vararg.annotation) if args.vararg.annotation else None
        params.append(("*" + args.vararg.arg, annotation))

    # Keyword-only args
    for arg in args.kwonlyargs:
        annotation = ast_to_source(arg.annotation) if arg.annotation else None
        params.append((arg.arg, annotation))

    # **kwargs
    if args.kwarg:
        annotation = ast_to_source(args.kwarg.annotation) if args.kwarg.annotation else None
        params.append(("**" + args.kwarg.arg, annotation))

    return params

def generate_function_docstring(func: ast.FunctionDef, parent_class: Optional[str] = None) -> str:
    """
    Generate a professional-looking Google-style docstring skeleton for a function or method.
    """
    name = func.name
    params = extract_parameters(func)

    is_method = parent_class is not None
    is_init = is_method and name == "__init__"

    # Summary line
    if is_method and is_init:
        summary = f"Initialise an instance of `{parent_class}`."
    elif is_method:
        summary = f"Method `{name}` of `{parent_class}`."
    else:
        summary = f"{name.replace('_', ' ').capitalize()}."

    # If there is a return annotation
    return_ann = ast_to_source(func.returns) if func.returns else None

    lines: List[str] = []
    lines.append(summary)
    lines.append("")
    lines.append("This is an auto-generated docstring skeleton. "
                 "Please update the description and parameter details as appropriate.")

    # Args section
    doc_params = [
        (n, a)
        for (n, a) in params
        if not (is_method and n in ("self", "cls"))
    ]

    if doc_params:
        lines.append("")
        lines.append("Args:")
        for name, annotation in doc_params:
            if annotation:
                lines.append(f"    {name} ({annotation}): TODO: describe parameter.")
            else:
                lines.append(f"    {name}: TODO: describe parameter.")

    # Returns section - now with proper blank line handling
    if return_ann and return_ann.lower() != "none":
        lines.append("")
        lines.append("Returns:")
        lines.append(f"    {return_ann}: TODO: describe return value.")

    return "\n".join(lines)

def generate_class_docstring(cls: ast.ClassDef) -> str:
    """
    Generate a professional-looking Google-style docstring skeleton for a class.
    """
    name = cls.name
    summary = f"{name} class."

    lines = [
        summary,
        "This is an auto-generated docstring skeleton. "
        "Please update the description, attributes, and examples as needed.",
    ]
    return "\n".join(lines)


class DocstringInjector(ast.NodeTransformer):
    """
    AST transformer that injects docstrings into functions, async functions,
    and classes that do not already have one.
    """

    def __init__(self):
        super().__init__()
        self.class_stack: List[str] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        # Track current class name so we know whether functions are methods
        self.class_stack.append(node.name)

        # Add class docstring if missing
        if ast.get_docstring(node) is None and node.body:
            docstring = generate_class_docstring(node)
            expr = ast.Expr(value=ast.Constant(value=docstring))
            node.body.insert(0, expr)

        # Process methods inside the class
        self.generic_visit(node)
        self.class_stack.pop()
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        parent_class = self.class_stack[-1] if self.class_stack else None

        if ast.get_docstring(node) is None and node.body:
            docstring = generate_function_docstring(node, parent_class=parent_class)
            expr = ast.Expr(value=ast.Constant(value=docstring))
            node.body.insert(0, expr)

        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        parent_class = self.class_stack[-1] if self.class_stack else None

        if ast.get_docstring(node) is None and node.body:
            docstring = generate_function_docstring(node, parent_class=parent_class)
            expr = ast.Expr(value=ast.Constant(value=docstring))
            node.body.insert(0, expr)

        self.generic_visit(node)
        return node


def process_file(input_path: str, output_path: str) -> None:
    """
    Read a Python file, inject docstring skeletons where missing, and
    write the result to a new file.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    transformer = DocstringInjector()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    try:
        new_source = ast.unparse(new_tree)  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "ast.unparse is not available. "
            "You need Python 3.9+ or install 'astor' and adapt the script."
        ) from exc

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_source)


def main():
    parser = argparse.ArgumentParser(
        description="Automatically generate Google-style docstring skeletons "
                    "for functions, methods and classes in a Python file."
    )
    parser.add_argument("input", help="Input Python file")
    parser.add_argument("output", help="Output Python file (with docstrings)")
    args = parser.parse_args()

    process_file(args.input, args.output)


if __name__ == "__main__":
    main()
