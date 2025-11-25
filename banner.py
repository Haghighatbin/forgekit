from pyfiglet import Figlet, FigletFont
from rich.console import Console
from src.configs.config import Config
from pathlib import Path

console = Console()

def Logo(version, author):
    font_path = Path(Config.FONT_DIR)
    font_name = '3d'
    try:
        if font_name not in FigletFont.getFonts():
            custom_font = font_path / f"{font_name}.flf"
            if not custom_font.is_file():
                raise FileNotFoundError(f"Font file '{custom_font}' not found.")
            FigletFont.installFonts(str(custom_font))

        f = Figlet(font=font_name, width=120, justify='left')
        console.print(f"[bold blue]{f.renderText('TickerTricker')}[/bold blue]")
        console.print(f"[bold blue]AUTHOR: {author}[/bold blue]")
        console.print(f"[bold blue]VERSION: {version}[/bold blue]\n")

    except Exception as e:
        console.print(f"[bold red]Error loading font: {e}[/bold red]")

